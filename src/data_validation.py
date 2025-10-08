import pandas as pd
from typing import Dict, Any

def validate_animal_data(animal: Dict[str, Any]) -> Dict[str, Any]:
    
    
    # Core fields for risk assessment
    critical_fields = ['size', 'age', 'attributes']
    
    # Count how many critical fields are present and complete
    complete_fields = 0
    total_fields = 0
    
    if animal.get('size'):
        complete_fields += 1
    total_fields += 1
    
    if animal.get('age'):
        complete_fields += 1
    total_fields += 1
    
    # Check attributes
    attrs = animal.get('attributes', {})
    attr_fields = ['energy_level', 'good_with_children', 'good_with_dogs', 'good_with_cats']
    for field in attr_fields:
        total_fields += 1
        if attrs.get(field) is not None:
            complete_fields += 1
    
    # Calculate confidence
    confidence_pct = (complete_fields / total_fields) * 100
    
    if confidence_pct >= 80:
        confidence = 'high'
    elif confidence_pct >= 50:
        confidence = 'medium'
    else:
        confidence = 'low'
    
    animal['data_confidence'] = confidence
    animal['data_completeness_pct'] = round(confidence_pct, 1)
    
    return animal

def get_conservative_defaults() -> Dict[str, str]:
    """Return conservative defaults for missing data"""
    return {
        'energy_level': 'unknown',
        'size': 'unknown',
        'age': 'unknown',
        'good_with_children': 'unknown',
        'good_with_dogs': 'unknown',
        'good_with_cats': 'unknown'
    }
