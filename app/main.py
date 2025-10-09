import streamlit as st
import sys
import os
import random
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

#adding root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db_helper import DatabaseHelper
from src.risk_engine import calculate_risk, rule_trigger_log, get_rule_trigger_stats
from src.adopter_profile import create_adopter_profile
from src.welcome_page import show_welcome_page
from src.app_styling import inject_professional_css, render_app_header, render_pet_card_header, render_metrics_header

# Initialize database helper

db_helper = DatabaseHelper()
count = db_helper.get_animal_count()

# Initialize session state for Tinder-style interface
if 'current_pet_index' not in st.session_state:
    st.session_state.current_pet_index = 0
if 'liked_pets' not in st.session_state:
    st.session_state.liked_pets = []
if 'passed_pets' not in st.session_state:
    st.session_state.passed_pets = []
if 'pet_queue' not in st.session_state:
    st.session_state.pet_queue = []
if 'last_action' not in st.session_state:
    st.session_state.last_action = None
if 'tutorial_completed' not in st.session_state:
    st.session_state.tutorial_completed = False

def get_pets_with_risk_scores(adopter_profile, limit=20):
    """Get pets sorted by risk level (low to high) with risk scores calculated"""
    conn = db_helper.get_connection()
    cursor = conn.cursor()
    
    # Get all adoptable pets including URL
    query = "SELECT id, name, type, species, breed, age, size, gender, description, url FROM animals WHERE status = 'adoptable'"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    pets_with_risk = []
    for row in rows:
        pet = {
            'id': row[0],
            'name': row[1],
            'type': row[2],
            'species': row[3],
            'breed': row[4],
            'age': row[5],
            'size': row[6],
            'gender': row[7],
            'description': row[8],
            'url': row[9]
        }
        
        # Get photo URL for this pet
        cursor.execute('SELECT photo_url FROM photos WHERE animal_id = ? LIMIT 1', (pet['id'],))
        photo_result = cursor.fetchone()
        pet['photo_url'] = photo_result[0] if photo_result else None
        # Calculate risk for this pet
        risk_result = calculate_risk(adopter_profile, pet)
        pet['risk_result'] = risk_result
        
        pets_with_risk.append(pet)
    
    conn.close()
    
    # Sort by risk score (low to high)
    pets_with_risk.sort(key=lambda x: x['risk_result']['risk_score'])
    
    return pets_with_risk[:limit]

def load_pet_queue(adopter_profile, batch_size=20):
    """Load a batch of pets into the queue"""
    if not st.session_state.pet_queue:
        st.session_state.pet_queue = get_pets_with_risk_scores(adopter_profile, batch_size)
    return st.session_state.pet_queue

def get_current_pet():
    """Get the current pet being displayed"""
    if st.session_state.pet_queue and st.session_state.current_pet_index < len(st.session_state.pet_queue):
        return st.session_state.pet_queue[st.session_state.current_pet_index]
    return None

def next_pet():
    """Move to the next pet in the queue"""
    st.session_state.current_pet_index += 1
    st.session_state.last_action = None

def like_pet(pet):
    """Add pet to liked pets and move to next"""
    if pet and pet['id'] not in [p['id'] for p in st.session_state.liked_pets]:
        st.session_state.liked_pets.append(pet)
    st.session_state.last_action = 'liked'
    next_pet()

def pass_pet(pet):
    """Add pet to passed pets and move to next"""
    if pet and pet['id'] not in [p['id'] for p in st.session_state.passed_pets]:
        st.session_state.passed_pets.append(pet)
    st.session_state.last_action = 'passed'
    next_pet()

def undo_last_action():
    """Undo the last action"""
    if st.session_state.last_action == 'liked' and st.session_state.liked_pets:
        st.session_state.liked_pets.pop()
        st.session_state.current_pet_index -= 1
    elif st.session_state.last_action == 'passed' and st.session_state.passed_pets:
        st.session_state.passed_pets.pop()
        st.session_state.current_pet_index -= 1
    st.session_state.last_action = None

def get_filtered_pets(species=None, age=None, size=None, gender=None):
    """Fetch pets from database with filters"""
    conn = db_helper.get_connection()
    cursor = conn.cursor()
    
    # Build query with filters
    query = "SELECT id, name, type, species, breed, age, size, gender, description FROM animals WHERE status = 'adoptable'"
    params = []
    
    if species:
        query += " AND species = ?"
        params.append(species)
    
    if age:
        query += " AND age = ?"
        params.append(age)
    
    if size:
        query += " AND size = ?"
        params.append(size)
    
    if gender:
        query += " AND gender = ?"
        params.append(gender)
    
    query += " ORDER BY name"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    pets = []
    for row in rows:
        pets.append({
            'id': row[0],
            'name': row[1],
            'type': row[2],
            'species': row[3],
            'breed': row[4],
            'age': row[5],
            'size': row[6],
            'gender': row[7],
            'description': row[8]
        })
    
    return pets

def get_risk_badge_color(risk_level):
    """Get color for risk badge based on risk level"""
    colors = {
        'Low': '#10b981',    # Emerald green
        'Medium': '#f59e0b', # Amber
        'High': '#ef4444'    # Red
    }
    return colors.get(risk_level, '#6b7280')  # Default gray

def display_pet_card(pet):
    """Display a compact pet card with action buttons at top"""
    if not pet:
        return
    
    risk_result = pet['risk_result']
    
    # Use container to prevent extra spacing
    with st.container():
        # Display photo if available, otherwise show placeholder
        if pet.get('photo_url'):
            st.image(pet['photo_url'], width=600)
        else:
            # No image placeholder
            st.markdown("""
            <div style="
                height: 300px;
                width: 100%;
                background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #94a3b8;
                font-size: 1.2rem;
                font-weight: 500;
                border: 2px dashed #cbd5e0;
                margin: 0;
            ">
                No Image Available
            </div>
            """, unsafe_allow_html=True)
        st.markdown("")
        
        # Pet name and risk badge using professional styling
        render_pet_card_header(pet['name'], risk_result['risk_level'])
    
        # Quick info row
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**{pet['species']} • {pet['age']}**")
        with col2:
            st.markdown(f"**{pet['size']} • {pet['gender']}**")
        with col3:
            st.markdown(f"**Match: {100 - risk_result['risk_score']}/100**")
        
        st.markdown("")
        
        # ACTION BUTTONS AT TOP - Most important actions
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("❤️ Like", key=f"like_{pet['id']}", type="primary", use_container_width=True):
                like_pet(pet)
                st.rerun()
        
        with col2:
            if st.button("❌ Pass", key=f"pass_{pet['id']}", type="secondary", use_container_width=True):
                pass_pet(pet)
                st.rerun()
        
        with col3:
            if pet.get('url'):
                st.link_button("🔗 View Listing", pet['url'], use_container_width=True)
    
        # Collapsible detailed information
        with st.expander("📝 View Full Details", expanded=False):
            # Data confidence badge
            confidence = 'high' if pet.get('breed') and pet.get('description') else 'medium' if pet.get('breed') else 'low'
            show_data_confidence_badge(confidence)
            
            st.markdown("---")
            
            # Detailed pet info
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Breed:** {pet['breed']}")
                st.markdown(f"**Age:** {pet['age']}")
                st.markdown(f"**Size:** {pet['size']}")
            
            with col2:
                st.markdown(f"**Gender:** {pet['gender']}")
                st.markdown(f"**Species:** {pet['species']}")
                st.markdown(f"**Compatibility:** {100 - risk_result['risk_score']}/100")
            
            st.markdown("---")
            
            # Risk summary
            st.markdown(f"**Match Summary:** {risk_result['summary']}")
            
            # Show concerns if any
            if risk_result['triggered_rules']:
                st.markdown("")
                st.markdown(f"**⚠ {len(risk_result['triggered_rules'])} Important Considerations:**")
                for i, rule in enumerate(risk_result['triggered_rules'][:3]):  # Show top 3
                    st.markdown(f"**{i+1}. {rule['rule_name']}**")
                    st.markdown(f"_{rule['concern']}_")
                    st.markdown("**What to do:**")
                    for guidance in rule['guidance'][:2]:  # Show first 2 guidance items
                        st.markdown(f"• {guidance}")
                    if i < len(risk_result['triggered_rules'][:3]) - 1:
                        st.markdown("")
            else:
                st.success("✅ Great match! No major concerns identified.")


# Old show_welcome_page() function removed - now using professional version from src/welcome_page.py

def load_metrics_data():
    """Load data for metrics dashboard"""
    conn = sqlite3.connect('db/app.db')
    
    # Get animals data
    query = """
        SELECT 
            id, name, species, age, size, distance,
            DATE(created_at) as date_added
        FROM animals 
        WHERE status = 'adoptable'
    """
    df = pd.read_sql_query(query, conn)
    
    # Get saved searches count
    searches_query = "SELECT COUNT(*) as count FROM saved_searches"
    searches_count = pd.read_sql_query(searches_query, conn)['count'][0]
    
    conn.close()
    return df, searches_count

def show_metrics_dashboard(df, searches_count, adopter_profile=None):
    """Display metrics dashboard with professional styling"""
    render_metrics_header("Adoption Inventory Insights")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Metric 1: Total available
    with col1:
        total = len(df)
        st.metric("Available Pets", f"{total:,}")
    
    # Metric 2: New today
    with col2:
        today = datetime.now().date()
        if 'date_added' in df.columns and df['date_added'].notna().any():
            new_today = len(df[pd.to_datetime(df['date_added']).dt.date == today])
        else:
            new_today = 0
        st.metric("New Today", new_today)
    
    # Metric 3: Median distance
    with col3:
        if 'distance' in df.columns and df['distance'].notna().any():
            median_dist = df['distance'].median()
            st.metric("Median Distance", f"{median_dist:.0f} mi")
        else:
            st.metric("Median Distance", "N/A")
    
    # Metric 4: Active searches
    with col4:
        st.metric("Active Searches", searches_count)
    
    # Additional insights
    if len(df) > 0:
        st.markdown("---")
        
        # Species breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("By Species")
            species_counts = df['species'].value_counts()
            for species, count in species_counts.items():
                pct = (count / total * 100)
                st.write(f"**{species}:** {count} ({pct:.1f}%)")
        
        with col2:
            st.subheader("By Age")
            age_counts = df['age'].value_counts()
            for age, count in age_counts.items():
                pct = (count / total * 100)
                st.write(f"**{age}:** {count} ({pct:.1f}%)")
        
        # Size distribution
        if 'size' in df.columns:
            st.subheader("By Size")
            size_counts = df['size'].value_counts()
            for size, count in size_counts.items():
                pct = (count / total * 100)
                st.write(f"**{size}:** {count} ({pct:.1f}%)")
    
    # Personalized insights based on adopter profile
    if adopter_profile:
        st.markdown("---")
        st.subheader("Personalized Insights")
        
        # Calculate compatibility for all pets
        compatible_pets = []
        for _, pet_row in df.iterrows():
            pet_data = {
                'id': pet_row['id'],
                'name': pet_row['name'],
                'species': pet_row['species'],
                'breed': 'Mixed',  # Default since we don't have breed in metrics
                'age': pet_row['age'],
                'size': pet_row['size'],
                'gender': 'Unknown',  # Default since we don't have gender in metrics
                'description': ''
            }
            
            risk_result = calculate_risk(adopter_profile, pet_data)
            if risk_result['risk_level'] == 'Low':
                compatible_pets.append(pet_data)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Low Risk Matches", len(compatible_pets))
        
        with col2:
            if total > 0:
                compatibility_rate = (len(compatible_pets) / total * 100)
                st.metric("Compatibility Rate", f"{compatibility_rate:.1f}%")
            else:
                st.metric("Compatibility Rate", "N/A")
        
        with col3:
            # Most common compatible species
            if compatible_pets:
                compatible_species = [pet['species'] for pet in compatible_pets]
                most_common = max(set(compatible_species), key=compatible_species.count)
                st.metric("Best Match Species", most_common)
            else:
                st.metric("Best Match Species", "N/A")

def show_rule_analytics():
    """Show which risk rules trigger most often"""
    if not rule_trigger_log:
        st.info("No risk assessments logged yet")
        return
    
    st.markdown("---")
    st.subheader("Most Common Risk Factors")
    
    # Count rule triggers
    rule_counts = {}
    for entry in rule_trigger_log:
        rule = entry['rule']
        rule_counts[rule] = rule_counts.get(rule, 0) + 1
    
    # Sort and display
    sorted_rules = sorted(rule_counts.items(), key=lambda x: x[1], reverse=True)
    
    for rule, count in sorted_rules[:10]:  # Top 10
        # Convert snake_case to readable
        readable = rule.replace('_', ' ').title()
        st.write(f"**{readable}**: {count} times")
    
    # Additional analytics
    stats = get_rule_trigger_stats()
    if stats:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Triggers", stats['total_triggers'])
        
        with col2:
            st.metric("Unique Rules", stats['unique_rules'])
        
        with col3:
            if stats['most_triggered']:
                most_rule, most_count = stats['most_triggered']
                readable_most = most_rule.replace('_', ' ').title()
                st.metric("Most Common", f"{readable_most} ({most_count})")
            else:
                st.metric("Most Common", "N/A")

def show_disclaimers_and_resources():
    """Display ethical disclaimers and professional resources"""
    
    with st.expander("Important: About Risk Guidance", expanded=False):
        st.markdown("""
        **Risk scores are guidance tools, not behavioral guarantees.**
        
        - These assessments are based on common adoption patterns and shelter research
        - Every pet is an individual with unique needs and personality
        - Missing data receives conservative ratings to avoid overconfidence
        - **Always meet pets in person** and consult with shelter staff
        
        For personalized support, connect with:
        - **Certified Professional Dog Trainers** (CPDT): [Find a Trainer](https://www.ccpdt.org/dog-owners/certified-dog-trainer-directory/)
        - **Veterinary Behaviorists** (DACVB): [Find a Behaviorist](https://www.dacvb.org/search/custom.asp?id=4709)
        - **Your local shelter's adoption counselors** for pet-specific insights
        """)
    
    st.markdown("---")

def show_data_confidence_badge(confidence):
    """Display data confidence indicator"""
    if confidence == 'high':
        st.success("✓ Complete Profile")
    elif confidence == 'medium':
        st.warning("⚠ Partial Profile")
    else:
        st.info("Limited Data - Visit shelter for details")

st.set_page_config(
    page_title="FurFindr - Smart Pet Adoption Matching", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject professional CSS
inject_professional_css()

# Check if user needs tutorial
if not st.session_state.tutorial_completed:
    show_welcome_page()
    st.stop()

# Render professional header
render_app_header()

# Sidebar for adopter profile and favorites
st.sidebar.header("Your Household Profile")
st.sidebar.write("Help us find the best pet match for you!")

with st.sidebar.form("adopter_profile_form"):
    st.subheader("Experience & Lifestyle")
    
    experience = st.selectbox("Experience Level", ["first_time", "some_experience", "experienced"], 
                             format_func=lambda x: {
                                 "first_time": "First-time owner",
                                 "some_experience": "Some experience", 
                                 "experienced": "Experienced"
                             }[x])
    
    
    exercise_time = st.slider(
        "Daily play time (minutes)",
        min_value=0,
        max_value=120,
        value=30,
        step=15
    )
    
    st.subheader("Household")
    
    has_kids = st.checkbox("I have children")
    kid_ages = []
    if has_kids:
        kid_ages = st.multiselect(
            "Children's ages",
            ["toddler", "school_age", "teen"],
            format_func=lambda x: {
                "toddler": "Toddler (0-4)",
                "school_age": "School age (5-12)",
                "teen": "Teen (13+)"
            }[x]
        )
    
    has_other_pets = st.checkbox("I have other pets")
    other_pet_types = []
    if has_other_pets:
        other_pet_types = st.multiselect(
            "What pets do you have?",
            ["dog", "cat", "small_animal", "bird"]
        )
    
    st.subheader("Home Environment")
    
    home_type = st.selectbox(
        "Home type",
        ["apartment", "townhouse", "house", "condo"]
    )
    
    yard_size = st.selectbox(
        "Yard size",
        ["none", "small", "medium", "large"]
    )
    
    st.subheader("Other Factors")
    
    work_schedule = st.selectbox(
        "Work schedule",
        ["full_time_office", "full_time_home", "part_time", "flexible", "retired"],
        format_func=lambda x: x.replace("_", " ").title()
    )
    
    allergies = st.selectbox(
        "Allergies to pets",
        ["none", "mild", "moderate", "severe"]
    )
    
    noise_tolerance = st.selectbox(
        "Noise tolerance",
        ["low", "medium", "high"],
        help="How tolerant are you/your neighbors of barking/noise?"
    )
    
    training_commitment = st.selectbox(
        "Training commitment",
        ["willing", "somewhat", "limited"],
        format_func=lambda x: {
            "willing": "Very willing to invest in training",
            "somewhat": "Somewhat willing",
            "limited": "Limited time for training"
        }[x]
    )
    
    submit = st.form_submit_button("Save your Profile")

# Store profile in session state
if submit:
    st.session_state.adopter_profile = create_adopter_profile(
        experience_level=experience,
        has_kids=has_kids,
        kid_ages=kid_ages,
        has_other_pets=has_other_pets,
        other_pet_types=other_pet_types,
        home_type=home_type,
        yard_size=yard_size,
        daily_exercise_minutes=exercise_time,
        work_schedule=work_schedule,
        allergies=allergies,
        noise_tolerance=noise_tolerance,
        training_commitment=training_commitment
    )
    st.sidebar.success("Profile saved! ✅")

# Favorites section in sidebar
st.sidebar.markdown("---")
st.sidebar.header("Your Favorites")

if st.session_state.liked_pets:
    st.sidebar.write(f"You've liked {len(st.session_state.liked_pets)} pets:")

    for i, pet in enumerate(st.session_state.liked_pets[-5:]):  # Show last 5
        with st.sidebar.expander("Favorite pet"):
            st.markdown(f"<div style='font-size:16px; font-weight:700; color:var(--text-color)'>{pet['name']}</div>", unsafe_allow_html=True)
            st.write(f"({pet['breed']})")
            st.write(f"**Risk Level:** {pet['risk_result']['risk_level']}")
            st.write(f"**Compatibility:** {100 - pet['risk_result']['risk_score']}/100")
            st.write(f"**Age:** {pet['age']} • **Size:** {pet['size']}")

            if pet['risk_result']['triggered_rules']:
                st.write(f"**Concerns:** {len(pet['risk_result']['triggered_rules'])}")
            else:
                st.success("Great match!")
            
            # Add view listing link
            if pet.get('url'):
                st.markdown(f"[View on PetFinder]({pet['url']})")
    
    if len(st.session_state.liked_pets) > 5:
        st.sidebar.caption(f"... and {len(st.session_state.liked_pets) - 5} more")
    
    if st.sidebar.button("Clear All Favorites"):
        st.session_state.liked_pets = []
        st.rerun()
    
    # Download options
    st.sidebar.markdown("---")
    st.sidebar.subheader("Download Options")
    
    # Download comprehensive report
    if st.sidebar.button("Download Complete Report", use_container_width=True, type="primary"):
        comprehensive_data = {
            "furfindr_report": {
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "session_stats": {
                    "total_pets_reviewed": len(st.session_state.liked_pets) + len(st.session_state.passed_pets),
                    "pets_liked": len(st.session_state.liked_pets),
                    "pets_passed": len(st.session_state.passed_pets),
                    "current_pet_index": st.session_state.current_pet_index
                },
                "adopter_profile": st.session_state.adopter_profile,
                "favorites": [
                    {
                        "name": pet["name"],
                        "breed": pet["breed"],
                        "age": pet["age"],
                        "size": pet["size"],
                        "gender": pet["gender"],
                        "species": pet["species"],
                        "risk_level": pet["risk_result"]["risk_level"],
                        "compatibility_score": 100 - pet["risk_result"]["risk_score"],
                        "risk_score": pet["risk_result"]["risk_score"],
                        "summary": pet["risk_result"]["summary"],
                        "concerns": len(pet["risk_result"]["triggered_rules"]),
                        "triggered_rules": [
                            {
                                "rule_name": rule["rule_name"],
                                "concern": rule["concern"],
                                "guidance": rule["guidance"]
                            } for rule in pet["risk_result"]["triggered_rules"]
                        ]
                    } for pet in st.session_state.liked_pets
                ]
            }
        }
        
        import json
        report_json = json.dumps(comprehensive_data, indent=2)
        
        st.sidebar.download_button(
            label="⬇️ Download Complete Report",
            data=report_json,
            file_name=f"furfindr_complete_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Individual download options
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("Profile", use_container_width=True):
            profile_data = {
                "adopter_profile": st.session_state.adopter_profile,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "session_stats": {
                    "total_pets_reviewed": len(st.session_state.liked_pets) + len(st.session_state.passed_pets),
                    "pets_liked": len(st.session_state.liked_pets),
                    "pets_passed": len(st.session_state.passed_pets)
                }
            }
            
            import json
            profile_json = json.dumps(profile_data, indent=2)
            
            st.download_button(
                label="⬇️ Download Profile",
                data=profile_json,
                file_name=f"furfindr_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("Favorites", use_container_width=True):
            if st.session_state.liked_pets:
                favorites_data = {
                    "favorites": [
                        {
                            "name": pet["name"],
                            "breed": pet["breed"],
                            "age": pet["age"],
                            "size": pet["size"],
                            "gender": pet["gender"],
                            "species": pet["species"],
                            "risk_level": pet["risk_result"]["risk_level"],
                            "compatibility_score": 100 - pet["risk_result"]["risk_score"],
                            "risk_score": pet["risk_result"]["risk_score"],
                            "summary": pet["risk_result"]["summary"],
                            "concerns": len(pet["risk_result"]["triggered_rules"]),
                            "triggered_rules": [
                                {
                                    "rule_name": rule["rule_name"],
                                    "concern": rule["concern"],
                                    "guidance": rule["guidance"]
                                } for rule in pet["risk_result"]["triggered_rules"]
                            ]
                        } for pet in st.session_state.liked_pets
                    ],
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "total_favorites": len(st.session_state.liked_pets)
                }
                
                import json
                favorites_json = json.dumps(favorites_data, indent=2)
                
                st.download_button(
                    label="⬇️ Download Favorites",
                    data=favorites_json,
                    file_name=f"furfindr_favorites_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("No favorites to download yet!")

else:
    st.sidebar.info("No pets liked yet. Start browsing to find your favorites!")

# Initialize default profile if none exists
if 'adopter_profile' not in st.session_state:
    st.session_state.adopter_profile = create_adopter_profile()

# Main Tinder-style interface
# Load pet queue if needed
load_pet_queue(st.session_state.adopter_profile, 20)

# Get current pet
current_pet = get_current_pet()

# Progress indicator
total_pets = len(st.session_state.pet_queue)
current_index = st.session_state.current_pet_index
remaining_pets = total_pets - current_index

if current_pet:
    # Progress bar
    progress = current_index / total_pets if total_pets > 0 else 0
    st.progress(progress)
    st.caption(f"Pet {current_index + 1} of {total_pets} • {remaining_pets} remaining")
    
    # Main pet card with action buttons at top
    display_pet_card(current_pet)
    
    # Show disclaimers and resources
    show_disclaimers_and_resources()
    
    # Undo button (only show if there was a recent action)
    if st.session_state.last_action:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Undo Last Action", type="secondary"):
                undo_last_action()
                st.rerun()
    
    # Stats
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pets Liked", len(st.session_state.liked_pets))
    with col2:
        st.metric("Pets Passed", len(st.session_state.passed_pets))
    with col3:
        st.metric("Remaining", remaining_pets)

else:
    # End of queue or no pets
    if total_pets == 0:
        st.info("No pets available. Please check back later!")
    else:
        st.success("You've reviewed all available pets!")
        st.write(f"You liked {len(st.session_state.liked_pets)} pets and passed on {len(st.session_state.passed_pets)} pets.")
        
        if st.button("Start Over", type="primary"):
            st.session_state.current_pet_index = 0
            st.session_state.pet_queue = []
            st.session_state.liked_pets = []
            st.session_state.passed_pets = []
            st.rerun()

# Load and show metrics AFTER the pet browsing section
df_metrics, searches_count = load_metrics_data()
show_metrics_dashboard(df_metrics, searches_count, st.session_state.adopter_profile)
