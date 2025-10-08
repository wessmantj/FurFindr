"""
Retention-Risk Engine
Evaluates adopter-pet compatibility based on research-backed friction patterns
"""

import json
from datetime import datetime
from .db_helper import DatabaseHelper

# Global rule trigger log for analytics (no PII)
rule_trigger_log = []

def log_rule_trigger(rule_name: str):
    """Log which rules are triggered (no PII)"""
    rule_trigger_log.append({
        'rule': rule_name,
        'timestamp': datetime.now().isoformat()
    })

def get_rule_trigger_stats():
    """Get statistics about rule triggers"""
    if not rule_trigger_log:
        return {}
    
    rule_counts = {}
    for entry in rule_trigger_log:
        rule_name = entry['rule']
        rule_counts[rule_name] = rule_counts.get(rule_name, 0) + 1
    
    return {
        'total_triggers': len(rule_trigger_log),
        'unique_rules': len(rule_counts),
        'rule_frequency': rule_counts,
        'most_triggered': max(rule_counts.items(), key=lambda x: x[1]) if rule_counts else None
    }

def clear_rule_log():
    """Clear the rule trigger log"""
    global rule_trigger_log
    rule_trigger_log = []


# Breed classification lists (keywords to search for)
HIGH_ENERGY_BREEDS = [
    'husky', 'border collie', 'australian shepherd', 'jack russell', 
    'cattle dog', 'malinois', 'pointer', 'setter', 'retriever', 'weimaraner',
    'springer spaniel', 'vizsla', 'dalmatian', 'boxer'
]

WORKING_HERDING_BREEDS = [
    'border collie', 'australian shepherd', 'cattle dog', 'german shepherd',
    'belgian malinois', 'collie', 'corgi', 'heeler', 'sheepdog'
]

VOCAL_BREEDS = [
    'husky', 'beagle', 'hound', 'chihuahua', 'terrier', 'schnauzer',
    'pomeranian', 'dachshund', 'basset', 'coonhound'
]

HEAVY_SHEDDERS = [
    'husky', 'german shepherd', 'golden retriever', 'labrador', 'corgi',
    'chow', 'akita', 'malamute', 'samoyed', 'saint bernard'
]

STUBBORN_INDEPENDENT_BREEDS = [
    'husky', 'shiba inu', 'basenji', 'chow', 'afghan hound',
    'terrier', 'bulldog', 'beagle', 'dachshund', 'pekingese'
]


def is_high_energy(pet_data):
    """Determine if pet is likely high-energy"""
    breed = pet_data.get('breed', '').lower()
    age = pet_data.get('age', '')
    size = pet_data.get('size', '')
    
    # Check breed keywords
    for keyword in HIGH_ENERGY_BREEDS:
        if keyword in breed:
            return True
    
    # Young + Large = likely high energy
    if age in ['Baby', 'Young'] and size in ['Large', 'Extra Large']:
        return True
    
    return False


def is_working_herding_breed(pet_data):
    """Check if pet is a working or herding breed"""
    breed = pet_data.get('breed', '').lower()
    
    for keyword in WORKING_HERDING_BREEDS:
        if keyword in breed:
            return True
    
    return False


def is_vocal_breed(pet_data):
    """Check if pet is prone to being vocal"""
    breed = pet_data.get('breed', '').lower()
    
    for keyword in VOCAL_BREEDS:
        if keyword in breed:
            return True
    
    return False


def is_heavy_shedder(pet_data):
    """Check if pet is a heavy shedding breed"""
    breed = (pet_data.get('breed') or '').lower()
    description = (pet_data.get('description') or '').lower()
    
    for keyword in HEAVY_SHEDDERS:
        if keyword in breed:
            return True
    
    # Check description mentions
    if 'sheds' in description or 'shedding' in description:
        return True
    
    return False


def is_stubborn_breed(pet_data):
    """Check if pet is known for being stubborn/independent"""
    breed = pet_data.get('breed', '').lower()
    
    for keyword in STUBBORN_INDEPENDENT_BREEDS:
        if keyword in breed:
            return True
    
    return False


def requires_only_pet(pet_data):
    """Check if pet must be only pet in household"""
    description = (pet_data.get('description') or '').lower()

    
    only_pet_keywords = [
        'only pet', 'no other animals', 'no other pets',
        'cat aggressive', 'dog aggressive', 'must be alone'
    ]
    
    for keyword in only_pet_keywords:
        if keyword in description:
            return True
    
    return False


def calculate_risk(adopter_profile, pet_data):
    """
    Calculate adoption retention risk based on adopter profile and pet traits
    
    Args:
        adopter_profile: Dictionary with adopter information
        pet_ Dictionary with pet information from database
    
    Returns:
        Dictionary with:
            - risk_score: Total risk points
            - risk_level: 'Low', 'Medium', or 'High'
            - triggered_rules: List of dicts with rule details
            - summary: Brief text summary
    """
    triggered_rules = []
    total_score = 0
    
    # Rule 1: First-Time Owner + High-Energy Pet
    if adopter_profile.get('experience_level') == 'first_time' and is_high_energy(pet_data):
        log_rule_trigger('first_time_high_energy')
        total_score += 25
        triggered_rules.append({
            'rule_name': 'First-Time Owner + High-Energy Pet',
            'concern': 'First-time owners often underestimate the time, energy, and training required for high-energy breeds. This can lead to behavioral issues and early returns.',
            'guidance': [
                'Enroll in puppy/dog training classes within first 2 weeks',
                'Commit to 60-90 minutes of daily exercise',
                'Research breed-specific needs and common challenges',
                'Join local dog owner groups for support'
            ],
            'weight': 25
        })
    
    # Rule 2: Young Children + Large Adolescent Dog
    if (adopter_profile.get('has_kids') and 
        'toddler' in adopter_profile.get('kid_ages', []) and
        pet_data.get('age') in ['Baby', 'Young'] and
        pet_data.get('size') in ['Large', 'Extra Large']):
        
        log_rule_trigger('young_children_large_dog')
        total_score += 40
        triggered_rules.append({
            'rule_name': 'Young Children + Large Adolescent Dog',
            'concern': 'Young dogs are naturally mouthy and jump. Large breeds can easily knock over small children, leading to injuries and fear.',
            'guidance': [
                'Work with certified trainer on gentle behavior from day one',
                'Supervise ALL interactions between child and pet',
                'Teach children proper pet handling',
                'Consider waiting until children are older or choosing smaller/calmer pet'
            ],
            'weight': 40
        })
    
    # Rule 3: Limited Exercise Time + Working/Herding Breed
    if (adopter_profile.get('daily_exercise_minutes', 0) < 30 and 
        is_working_herding_breed(pet_data)):
        
        log_rule_trigger('limited_exercise_working_breed')
        total_score += 35
        triggered_rules.append({
            'rule_name': 'Limited Exercise Time + Working/Herding Breed',
            'concern': 'Working breeds require significant physical and mental stimulation. Without it, they develop destructive behaviors, anxiety, and can become difficult to manage.',
            'guidance': [
                'Increase daily exercise commitment to minimum 60 minutes',
                'Add mental stimulation: puzzle toys, training sessions, nose work',
                'Consider doggy daycare 2-3 times per week',
                'Alternatively, choose a lower-energy breed better suited to lifestyle'
            ],
            'weight': 35
        })
    
    # Rule 4: Apartment Living + Very Vocal Breed
    if (adopter_profile.get('home_type') == 'apartment' and
        adopter_profile.get('noise_tolerance') == 'low' and
        is_vocal_breed(pet_data)):
        
        log_rule_trigger('apartment_vocal_breed')
        total_score += 20
        triggered_rules.append({
            'rule_name': 'Apartment Living + Very Vocal Breed',
            'concern': 'Vocal breeds are prone to barking, howling, and "talking." In apartments with shared walls, this leads to neighbor complaints and potential eviction.',
            'guidance': [
                'Budget for professional trainer specializing in quiet commands',
                'Start training immediately upon adoption',
                'Discuss with neighbors upfront about training period',
                'Consider soundproofing measures',
                'Choose quieter breed if noise is dealbreaker'
            ],
            'weight': 20
        })
    
    # Rule 5: Allergies + Heavy Shedding Breed
    if (adopter_profile.get('allergies') in ['mild', 'moderate', 'severe'] and
        is_heavy_shedder(pet_data)):
        
        log_rule_trigger('allergies_heavy_shedding')
        total_score += 30
        triggered_rules.append({
            'rule_name': 'Allergies + Heavy Shedding Breed',
            'concern': 'Even mild allergies can worsen with constant exposure to dander and shed fur. Severe cases force returns and can affect household health.',
            'guidance': [
                'Consult allergist before adoption',
                'Commit to weekly professional grooming',
                'Invest in HEPA air filters for home',
                'Keep pet out of bedrooms',
                'Consider hypoallergenic breeds (Poodle, Bichon, Portuguese Water Dog)'
            ],
            'weight': 30
        })
    
    # Rule 6: No Yard + Large High-Energy Dog
    if (adopter_profile.get('yard_size') == 'none' and
        adopter_profile.get('home_type') == 'apartment' and
        pet_data.get('size') in ['Large', 'Extra Large'] and
        pet_data.get('age') in ['Baby', 'Young']):
        
        log_rule_trigger('no_yard_large_high_energy')
        total_score += 20
        triggered_rules.append({
            'rule_name': 'No Yard + Large High-Energy Dog',
            'concern': 'Large dogs without outdoor space require multiple daily walks and dedicated exercise time. Easy to under-exercise, leading to behavior problems.',
            'guidance': [
                'Commit to 3+ walks daily (morning, midday, evening)',
                'Find nearby dog parks or trails',
                'Budget for dog walker if working full-time',
                'Consider smaller or lower-energy pet'
            ],
            'weight': 20
        })
    
    # Rule 7: Full-Time Office Work + Separation Anxiety Risk
    if (adopter_profile.get('work_schedule') == 'full_time_office' and
    (pet_data.get('age') == 'Baby' or 
     'shy' in (pet_data.get('description') or '').lower() or
     'anxious' in (pet_data.get('description') or '').lower())):

        
        log_rule_trigger('full_time_office_separation_anxiety')
        total_score += 25
        triggered_rules.append({
            'rule_name': 'Full-Time Office Work + Separation Anxiety Risk',
            'concern': 'Young puppies and anxious pets can develop separation anxiety when left alone for long periods. Results in destructive behavior and stress.',
            'guidance': [
                'Arrange for midday dog walker or pet sitter',
                'Consider doggy daycare 3-5 days per week',
                'Crate train properly from day one',
                'Start with shorter absences and gradually increase',
                'Choose more independent adult pet if schedule inflexible'
            ],
            'weight': 25
        })
    
    # Rule 8: No Other Pets + "Must Be Only Pet"
    if (adopter_profile.get('has_other_pets') and requires_only_pet(pet_data)):
        log_rule_trigger('has_pets_must_be_only')
        total_score += 50
        triggered_rules.append({
            'rule_name': 'Has Other Pets + Must Be Only Pet',
            'concern': 'Direct incompatibility. This pet\'s behavioral needs conflict with your household situation.',
            'guidance': [
                '⚠️ This is a dealbreaker - do not proceed with this match',
                'Search for pets marked as good with other animals',
                'Consult shelter staff if you still want to consider this pet'
            ],
            'weight': 50
        })
    
    # Rule 9: Limited Training Commitment + Strong-Willed Breed
    if (adopter_profile.get('training_commitment') == 'limited' and
        is_stubborn_breed(pet_data)):
        
        log_rule_trigger('limited_training_stubborn_breed')
        total_score += 20
        triggered_rules.append({
            'rule_name': 'Limited Training Commitment + Strong-Willed Breed',
            'concern': 'Independent breeds require consistent, patient training. Without commitment, they become unmanageable and develop bad habits.',
            'guidance': [
                'Reconsider training commitment - these breeds require structure',
                'Hire professional trainer if unable to commit personal time',
                'Choose easier-to-train breed (Golden Retriever, Lab, Poodle)',
                'Read breed-specific training resources before deciding'
            ],
            'weight': 20
        })
    
    # Rule 10: Senior Pet + First-Time Owner
    if (adopter_profile.get('experience_level') == 'first_time' and
        pet_data.get('age') == 'Senior'):
        
        log_rule_trigger('senior_pet_first_time_owner')
        total_score += 15
        triggered_rules.append({
            'rule_name': 'Senior Pet + First-Time Owner',
            'concern': 'Senior pets may have special medical needs, behavioral quirks from past experiences, and shorter lifespan. First-time owners may be unprepared for costs and emotional aspects.',
            'guidance': [
                'Research senior pet care and common health issues',
                'Budget for potential vet expenses (often higher for seniors)',
                'Understand end-of-life care may come sooner',
                'Consult with shelter about this specific senior\'s needs',
                '💙 Senior pets can be wonderful for prepared adopters!'
            ],
            'weight': 15
        })
    
    # Determine risk level based on score
    if total_score < 20:
        risk_level = "Low"
        summary = f"{pet_data.get('name', 'This pet')} appears to be a good match for your household!"
    elif total_score < 50:
        risk_level = "Medium"
        summary = f"{pet_data.get('name', 'This pet')} could work with preparation and commitment to the guidance below."
    else:
        risk_level = "High"
        summary = f"{pet_data.get('name', 'This pet')} presents significant challenges for your situation. Carefully review concerns before proceeding."
    
    return {
        'pet_name': pet_data.get('name', 'Unknown'),
        'pet_breed': pet_data.get('breed', 'Unknown'),
        'risk_score': total_score,
        'risk_level': risk_level,
        'summary': summary,
        'triggered_rules': triggered_rules,
        'total_rules_triggered': len(triggered_rules)
    }


def get_pet_by_id(pet_id):
    """Fetch a pet from database by ID"""
    db = DatabaseHelper()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, type, species, breed, age, size, gender, status,
               distance, description, organization_id, url
        FROM animals 
        WHERE id = ?
    ''', (pet_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'name': row[1],
            'type': row[2],
            'species': row[3],
            'breed': row[4],
            'age': row[5],
            'size': row[6],
            'gender': row[7],
            'status': row[8],
            'distance': row[9],
            'description': row[10],
            'organization_id': row[11],
            'url': row[12]
        }
    return None


def get_sample_pets(limit=5):
    """Fetch sample pets from database for testing"""
    db = DatabaseHelper()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, name, type, species, breed, age, size, gender, description
        FROM animals 
        WHERE type = 'Dog'
        LIMIT ?
    ''', (limit,))
    
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


def print_risk_report(result):
    """Pretty print a risk assessment result"""
    print("\n" + "="*70)
    print(f"🐾 ADOPTION COMPATIBILITY REPORT: {result['pet_name']}")
    print("="*70)
    print(f"\nBreed: {result['pet_breed']}")
    print(f"Risk Level: {result['risk_level']} (Score: {result['risk_score']}/100)")
    print(f"\n{result['summary']}")
    
    if result['triggered_rules']:
        print(f"\n⚠️  {result['total_rules_triggered']} Concern(s) Identified:\n")
        
        for i, rule in enumerate(result['triggered_rules'], 1):
            print(f"{i}. {rule['rule_name']} [{rule['weight']} points]")
            print(f"   Why this matters: {rule['concern']}")
            print(f"   What to do:")
            for guidance in rule['guidance']:
                print(f"      • {guidance}")
            print()
    else:
        print("\n✅ No major compatibility concerns identified!")
        print("This pet appears well-suited to your household situation.")
    
    print("="*70 + "\n")


if __name__ == "__main__":
    from .adopter_profile import SAMPLE_PROFILES
    
    print("RETENTION-RISK ENGINE TEST\n")
    
    # Get some real pets from database
    pets = get_sample_pets(3)
    
    if not pets:
        print("❌ No pets found in database. Run ETL first: python etl/run_daily.py")
    else:
        # Test each sample profile against first pet
        test_pet = pets[0]
        print(f"Testing against: {test_pet['name']} ({test_pet['breed']})\n")
        
        for profile_name, profile in SAMPLE_PROFILES.items():
            print(f"\n{'='*70}")
            print(f"PROFILE: {profile_name.upper().replace('_', ' ')}")
            print(f"{'='*70}")
            
            result = calculate_risk(profile, test_pet)
            print_risk_report(result)
        
        # Show one more detailed example
        print("\n\n" + "="*70)
        print("DETAILED EXAMPLE: High-Risk Profile vs Young Husky")
        print("="*70)
        
        # Create a challenging scenario
        high_risk_profile = SAMPLE_PROFILES['high_risk']
        
        # Create a challenging pet (simulated)
        challenging_pet = {
            'id': 'test123',
            'name': 'Storm',
            'type': 'Dog',
            'species': 'Dog',
            'breed': 'Siberian Husky',
            'age': 'Young',
            'size': 'Large',
            'gender': 'Male',
            'description': 'High-energy Husky who loves to talk! Needs experienced owner.',
            'status': 'adoptable'
        }
        
        result = calculate_risk(high_risk_profile, challenging_pet)
        print_risk_report(result)
