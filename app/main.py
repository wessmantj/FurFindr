import streamlit as st
import sys
import os

#adding root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.db_helper import DatabaseHelper
from src.risk_engine import calculate_risk
from src.adopter_profile import create_adopter_profile

# Initialize database helper
db_helper = DatabaseHelper()
count = db_helper.get_animal_count()

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
        'Low': '#28a745',    # Green
        'Medium': '#ffc107', # Yellow
        'High': '#dc3545'    # Red
    }
    return colors.get(risk_level, '#6c757d')  # Default gray

st.set_page_config(page_title="FurFinder - Your Smart Matched Pet Adoption", layout="wide")

st.title("FurFinder")
st.subheader("Find your perfect pet match with specialized guidance")

st.write(f"Currently showing {count} adoptable pets from the database.")

# Sidebar for adopter profile input
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
        "Daily exercise time (minutes)",
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
        ["apartment", "townhouse", "house"]
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

# Initialize default profile if none exists
if 'adopter_profile' not in st.session_state:
    st.session_state.adopter_profile = create_adopter_profile()

# Main area - Filters
st.header("🔎 Browse Adoptable Pets")

col1, col2, col3, col4 = st.columns(4)

with col1:
    filter_species = st.selectbox(
        "Species",
        ["All", "Dog", "Cat"],
        key="species_filter"
    )

with col2:
    filter_age = st.selectbox(
        "Age",
        ["All", "Baby", "Young", "Adult", "Senior"],
        key="age_filter"
    )

with col3:
    filter_size = st.selectbox(
        "Size",
        ["All", "Small", "Medium", "Large", "Extra Large"],
        key="size_filter"
    )

with col4:
    filter_gender = st.selectbox(
        "Gender",
        ["All", "Male", "Female"],
        key="gender_filter"
    )

# Fetch pets based on filters
pets = get_filtered_pets(
    species=filter_species if filter_species != "All" else None,
    age=filter_age if filter_age != "All" else None,
    size=filter_size if filter_size != "All" else None,
    gender=filter_gender if filter_gender != "All" else None
)

st.write(f"Showing {len(pets)} pets")

# Display pets in grid
if pets:
    # Create columns for grid layout (3 per row)
    for i in range(0, len(pets), 3):
        cols = st.columns(3)
        
        for j, col in enumerate(cols):
            if i + j < len(pets):
                pet = pets[i + j]
                
                # Calculate risk for this pet
                risk_result = calculate_risk(st.session_state.adopter_profile, pet)
                
                with col:
                    # Pet card
                    with st.container():
                        st.subheader(f"🐾 {pet['name']}")
                        
                        # Risk badge
                        badge_color = get_risk_badge_color(risk_result['risk_level'])
                        st.markdown(
                            f"<span style='background-color: {badge_color}; color: white; "
                            f"padding: 5px 10px; border-radius: 5px; font-weight: bold;'>"
                            f"{risk_result['risk_level']} Risk</span>",
                            unsafe_allow_html=True
                        )
                        
                        # Pet details
                        st.write(f"**Breed:** {pet['breed']}")
                        st.write(f"**Age:** {pet['age']} • **Size:** {pet['size']}")
                        st.write(f"**Gender:** {pet['gender']}")
                        
                        # Risk expander
                        with st.expander(f"🔍 Why {risk_result['risk_level']} risk?"):
                            st.write(f"**Score:** {risk_result['risk_score']}/100")
                            st.write(risk_result['summary'])
                            
                            if risk_result['triggered_rules']:
                                st.write("---")
                                st.write("**⚠️ Concerns:**")
                                
                                for rule in risk_result['triggered_rules']:
                                    st.write(f"**{rule['rule_name']}**")
                                    st.write(f"_{rule['concern']}_")
                                    
                                    st.write("**What to do:**")
                                    for guidance in rule['guidance']:
                                        st.write(f"• {guidance}")
                                    
                                    st.write("")
                            else:
                                st.success("✅ No major concerns! This pet seems well-suited to your household.")
                        
                        st.write("---")
else:
    st.info("No pets match your filters. Try adjusting your search criteria.")
    
# Adoption Support Section
st.header("📋 Post-Adoption Support")

col1, col2 = st.columns(2)

with col1:
    st.subheader("First-Week Checklist")
    st.write("Prepare for a successful start with your new pet!")
    
    pet_name_input = st.text_input("Pet's name (optional)", value="Your New Pet")
    pet_type_input = st.selectbox("Pet type", ["Dog", "Cat", "Other"])
    
    if st.button("📥 Generate Checklist PDF"):
        from src.adoption_checklist import generate_checklist_pdf
        
        with st.spinner("Generating your personalized checklist..."):
            pdf_path = generate_checklist_pdf(
                pet_name=pet_name_input,
                pet_type=pet_type_input,
                output_path=f"checklist_{pet_name_input.replace(' ', '_')}.pdf"
            )
            
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="⬇️ Download Checklist",
                    data=file,
                    file_name=f"{pet_name_input}_FirstWeek_Checklist.pdf",
                    mime="application/pdf"
                )
            
            st.success("✅ Checklist ready! Click above to download.")

with col2:
    st.subheader("Need Help?")
    st.write("Common resources for new pet parents:")
    st.markdown("""
    - **Training:** ASPCA Virtual Behaviorist
    - **Vet Questions:** AskVet, Vetster (telehealth)
    - **Behavior Issues:** Find a CAAB certified behaviorist
    - **Community:** Join local pet parent groups
    """)

# Comparison feature
st.header("⚖️ Compare Two Pets")

if pets and len(pets) >= 2:
    col1, col2 = st.columns(2)
    
    with col1:
        pet1_options = {f"{p['name']} ({p['breed']})": p for p in pets}
        pet1_selection = st.selectbox("Select first pet", list(pet1_options.keys()), key="pet1")
        pet1 = pet1_options[pet1_selection]
    
    with col2:
        pet2_options = {f"{p['name']} ({p['breed']})": p for p in pets if p['id'] != pet1['id']}
        if pet2_options:
            pet2_selection = st.selectbox("Select second pet", list(pet2_options.keys()), key="pet2")
            pet2 = pet2_options[pet2_selection]
        else:
            st.warning("Select a different first pet to compare")
            pet2 = None
    
    if pet2 and st.button("Compare Pets"):
        # Calculate risks
        risk1 = calculate_risk(st.session_state.adopter_profile, pet1)
        risk2 = calculate_risk(st.session_state.adopter_profile, pet2)
        
        # Display comparison
        st.subheader("Comparison Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"### 🐾 {pet1['name']}")
            st.write(f"**{pet1['breed']}**")
            st.write(f"{pet1['age']} • {pet1['size']} • {pet1['gender']}")
            
            badge_color = get_risk_badge_color(risk1['risk_level'])
            st.markdown(
                f"<h2 style='color: {badge_color};'>{risk1['risk_level']} Risk</h2>",
                unsafe_allow_html=True
            )
            st.write(f"**Score:** {risk1['risk_score']}/100")
            
            if risk1['triggered_rules']:
                st.write(f"**{len(risk1['triggered_rules'])} Concerns:**")
                for rule in risk1['triggered_rules']:
                    st.write(f"• {rule['rule_name']}")
            else:
                st.success("✅ No major concerns")
        
        with col2:
            st.write(f"### 🐾 {pet2['name']}")
            st.write(f"**{pet2['breed']}**")
            st.write(f"{pet2['age']} • {pet2['size']} • {pet2['gender']}")
            
            badge_color = get_risk_badge_color(risk2['risk_level'])
            st.markdown(
                f"<h2 style='color: {badge_color};'>{risk2['risk_level']} Risk</h2>",
                unsafe_allow_html=True
            )
            st.write(f"**Score:** {risk2['risk_score']}/100")
            
            if risk2['triggered_rules']:
                st.write(f"**{len(risk2['triggered_rules'])} Concerns:**")
                for rule in risk2['triggered_rules']:
                    st.write(f"• {rule['rule_name']}")
            else:
                st.success("✅ No major concerns")
        
        # Winner
        st.write("---")
        if risk1['risk_score'] < risk2['risk_score']:
            st.success(f"🏆 {pet1['name']} appears to be the better match for your household!")
        elif risk2['risk_score'] < risk1['risk_score']:
            st.success(f"🏆 {pet2['name']} appears to be the better match for your household!")
        else:
            st.info(f"Both pets have similar compatibility scores. Review individual concerns above.")
else:
    st.info("Need at least 2 pets to compare. Adjust your filters if needed.")

# Save search feature in sidebar
st.sidebar.write("---")
st.sidebar.subheader("💾 Save This Search")

with st.sidebar.form("save_search_form"):
    search_name = st.text_input("Search name", placeholder="e.g., 'My ideal dog'")
    search_email = st.text_input("Email for alerts", placeholder="your@email.com")
    
    save_button = st.form_submit_button("💾 Save & Get Alerts")
    
    if save_button:
        if not search_name or not search_email:
            st.error("Please provide both name and email")
        else:
            from src.saved_search_helper import save_search
            
            # Get current filters
            current_filters = {
                'species': st.session_state.get('species_filter', 'All'),
                'age': st.session_state.get('age_filter', 'All'),
                'size': st.session_state.get('size_filter', 'All'),
                'gender': st.session_state.get('gender_filter', 'All')
            }
            
            try:
                search_id = save_search(
                    email=search_email,
                    name=search_name,
                    adopter_profile=st.session_state.adopter_profile,
                    filters=current_filters
                )
                st.success(f"✅ Search saved! You'll receive daily email updates.")
            except Exception as e:
                st.error(f"Error saving search: {e}")