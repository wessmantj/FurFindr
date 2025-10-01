"""
Test script for retention-risk engine
Tests various adopter-pet combinations
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.risk_engine import calculate_risk, get_sample_pets, print_risk_report
from src.adopter_profile import create_adopter_profile, SAMPLE_PROFILES

def test_all_profiles_against_pet(pet):
    """Test all sample profiles against one pet"""
    print(f"\n{'='*70}")
    print(f"TESTING PET: {pet['name']} - {pet['breed']} ({pet['age']}, {pet['size']})")
    print(f"{'='*70}\n")
    
    for profile_name, profile in SAMPLE_PROFILES.items():
        print(f"\nProfile: {profile_name.replace('_', ' ').title()}")
        print("-" * 50)
        
        result = calculate_risk(profile, pet)
        
        print(f"Risk Level: {result['risk_level']} ({result['risk_score']} points)")
        print(f"Rules Triggered: {result['total_rules_triggered']}")
        
        if result['triggered_rules']:
            for rule in result['triggered_rules']:
                print(f"  - {rule['rule_name']}")


def test_specific_scenarios():
    """Test specific edge cases and scenarios"""
    print("\n" + "="*70)
    print("SPECIFIC SCENARIO TESTS")
    print("="*70)
    
    # Scenario 1: Perfect match
    print("\n1. IDEAL SCENARIO: Experienced owner + calm senior dog")
    print("-" * 50)
    
    perfect_adopter = create_adopter_profile(
        experience_level='experienced',
        home_type='house',
        yard_size='large',
        daily_exercise_minutes=60,
        allergies='none',
        training_commitment='willing'
    )
    
    calm_senior = {
        'name': 'Buddy',
        'breed': 'Golden Retriever Mix',
        'age': 'Senior',
        'size': 'Large',
        'description': 'Calm, friendly senior dog. Great with families.'
    }
    
    result = calculate_risk(perfect_adopter, calm_senior)
    print(f"Result: {result['risk_level']} risk ({result['risk_score']} points)")
    print(f"Summary: {result['summary']}\n")
    
    # Scenario 2: Multiple red flags
    print("\n2. CHALLENGING SCENARIO: First-timer + high-energy husky puppy")
    print("-" * 50)
    
    challenging_adopter = create_adopter_profile(
        experience_level='first_time',
        home_type='apartment',
        yard_size='none',
        daily_exercise_minutes=20,
        work_schedule='full_time_office',
        training_commitment='limited'
    )
    
    husky_puppy = {
        'name': 'Luna',
        'breed': 'Siberian Husky',
        'age': 'Baby',
        'size': 'Large',
        'description': 'Energetic husky puppy, very vocal!'
    }
    
    result = calculate_risk(challenging_adopter, husky_puppy)
    print(f"Result: {result['risk_level']} risk ({result['risk_score']} points)")
    print(f"Rules triggered: {result['total_rules_triggered']}")
    for rule in result['triggered_rules']:
        print(f"  - {rule['rule_name']} [{rule['weight']} pts]")
    
    # Scenario 3: Dealbreaker
    print("\n3. DEALBREAKER SCENARIO: Has cats + cat-aggressive dog")
    print("-" * 50)
    
    multi_pet_home = create_adopter_profile(
        experience_level='experienced',
        has_other_pets=True,
        other_pet_types=['cat']
    )
    
    cat_aggressive = {
        'name': 'Rex',
        'breed': 'Terrier Mix',
        'age': 'Adult',
        'size': 'Medium',
        'description': 'Great dog but must be only pet. Cat aggressive.'
    }
    
    result = calculate_risk(multi_pet_home, cat_aggressive)
    print(f"Result: {result['risk_level']} risk ({result['risk_score']} points)")
    print(f"⚠️  DEALBREAKER DETECTED")
    
    # Scenario 4: Moderate with mitigations
    print("\n4. MODERATE SCENARIO: Some experience + energetic young dog")
    print("-" * 50)
    
    moderate_adopter = create_adopter_profile(
        experience_level='some_experience',
        home_type='house',
        yard_size='medium',
        daily_exercise_minutes=45,
        training_commitment='willing'
    )
    
    active_dog = {
        'name': 'Charlie',
        'breed': 'Australian Shepherd Mix',
        'age': 'Young',
        'size': 'Medium',
        'description': 'Smart, active dog who loves to play'
    }
    
    result = calculate_risk(moderate_adopter, active_dog)
    print(f"Result: {result['risk_level']} risk ({result['risk_score']} points)")
    print(f"Summary: {result['summary']}")


def test_with_real_database_pets():
    """Test with actual pets from database"""
    print("\n" + "="*70)
    print("TESTING WITH REAL DATABASE PETS")
    print("="*70)
    
    pets = get_sample_pets(5)
    
    if not pets:
        print("\n❌ No pets in database. Run ETL first: python etl/run_daily.py")
        return
    
    print(f"\nFound {len(pets)} pets in database\n")
    
    # Test high-risk profile against each pet
    high_risk = SAMPLE_PROFILES['high_risk']
    
    print("Testing HIGH RISK profile against all pets:\n")
    
    for pet in pets:
        result = calculate_risk(high_risk, pet)
        print(f"• {pet['name']} ({pet['breed']}): {result['risk_level']} "
              f"({result['risk_score']} pts, {result['total_rules_triggered']} concerns)")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("RETENTION-RISK ENGINE - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    # Run all tests
    test_specific_scenarios()
    test_with_real_database_pets()
    
    # Detailed example
    print("\n\n" + "="*70)
    print("DETAILED REPORT EXAMPLE")
    print("="*70)
    
    pets = get_sample_pets(1)
    if pets:
        test_pet = pets[0]
        test_profile = SAMPLE_PROFILES['high_risk']
        
        result = calculate_risk(test_profile, test_pet)
        print_risk_report(result)
