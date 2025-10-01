"""
Adopter Profile Schema
Defines the structure for capturing adopter information
"""

def create_adopter_profile(
    experience_level='first_time',
    has_kids=False,
    kid_ages=None,
    has_other_pets=False,
    other_pet_types=None,
    home_type='apartment',
    yard_size='none',
    daily_exercise_minutes=30,
    work_schedule='full_time_office',
    allergies='none',
    noise_tolerance='medium',
    training_commitment='willing'
):
    """
    Create a standardized adopter profile
    
    Args:
        experience_level: 'first_time', 'some_experience', 'experienced'
        has_kids: Boolean
        kid_ages: List of age groups: 'toddler' (0-4), 'school_age' (5-12), 'teen' (13+)
        has_other_pets: Boolean
        other_pet_types: List: 'dog', 'cat', 'small_animal', 'bird'
        home_type: 'apartment', 'townhouse', 'house'
        yard_size: 'none', 'small', 'medium', 'large'
        daily_exercise_minutes: Integer (0-120+)
        work_schedule: 'full_time_office', 'full_time_home', 'part_time', 'flexible', 'retired'
        allergies: 'none', 'mild', 'moderate', 'severe'
        noise_tolerance: 'low', 'medium', 'high'
        training_commitment: 'willing', 'somewhat', 'limited'
    
    Returns:
        Dictionary with adopter profile
    """
    if kid_ages is None:
        kid_ages = []
    if other_pet_types is None:
        other_pet_types = []
    
    return {
        'experience_level': experience_level,
        'has_kids': has_kids,
        'kid_ages': kid_ages,
        'has_other_pets': has_other_pets,
        'other_pet_types': other_pet_types,
        'home_type': home_type,
        'yard_size': yard_size,
        'daily_exercise_minutes': daily_exercise_minutes,
        'work_schedule': work_schedule,
        'allergies': allergies,
        'noise_tolerance': noise_tolerance,
        'training_commitment': training_commitment
    }


# Example profiles for testing
SAMPLE_PROFILES = {
    'ideal_match': create_adopter_profile(
        experience_level='experienced',
        home_type='house',
        yard_size='large',
        daily_exercise_minutes=90,
        work_schedule='flexible',
        allergies='none',
        training_commitment='willing'
    ),
    
    'high_risk': create_adopter_profile(
        experience_level='first_time',
        has_kids=True,
        kid_ages=['toddler'],
        home_type='apartment',
        yard_size='none',
        daily_exercise_minutes=15,
        work_schedule='full_time_office',
        allergies='moderate',
        noise_tolerance='low',
        training_commitment='limited'
    ),
    
    'moderate_risk': create_adopter_profile(
        experience_level='some_experience',
        has_kids=True,
        kid_ages=['school_age'],
        home_type='townhouse',
        yard_size='small',
        daily_exercise_minutes=45,
        work_schedule='part_time',
        allergies='none',
        training_commitment='willing'
    )
}


if __name__ == "__main__":
    print("Sample Adopter Profiles:\n")
    
    for profile_name, profile in SAMPLE_PROFILES.items():
        print(f"{profile_name.upper().replace('_', ' ')}:")
        for key, value in profile.items():
            print(f"  {key}: {value}")
        print()
