"""
Saved Search Management
Functions to store and retrieve user search preferences
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
import json
from datetime import datetime
from src.db_helper import DatabaseHelper


import sqlite3
import json
from datetime import datetime
from src.db_helper import DatabaseHelper


def save_search(email, name, adopter_profile, filters=None):
    """
    Save a user's search preferences
    
    Args:
        email: User's email address
        name: Name for this saved search
        adopter_profile: Dictionary with adopter information
        filters: Optional dict with species, age, size, gender filters
    
    Returns:
        ID of saved search
    """
    db = DatabaseHelper()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    if filters is None:
        filters = {}
    
    # Convert lists to JSON strings for storage
    kid_ages_json = json.dumps(adopter_profile.get('kid_ages', []))
    other_pet_types_json = json.dumps(adopter_profile.get('other_pet_types', []))
    
    cursor.execute('''
        INSERT INTO saved_searches 
        (email, name, experience_level, has_kids, kid_ages, has_other_pets, 
         other_pet_types, home_type, yard_size, daily_exercise_minutes, 
         work_schedule, allergies, noise_tolerance, training_commitment,
         species, age, size, gender, max_distance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        email,
        name,
        adopter_profile.get('experience_level'),
        1 if adopter_profile.get('has_kids') else 0,
        kid_ages_json,
        1 if adopter_profile.get('has_other_pets') else 0,
        other_pet_types_json,
        adopter_profile.get('home_type'),
        adopter_profile.get('yard_size'),
        adopter_profile.get('daily_exercise_minutes'),
        adopter_profile.get('work_schedule'),
        adopter_profile.get('allergies'),
        adopter_profile.get('noise_tolerance'),
        adopter_profile.get('training_commitment'),
        filters.get('species'),
        filters.get('age'),
        filters.get('size'),
        filters.get('gender'),
        filters.get('max_distance')
    ))
    
    search_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return search_id


def get_saved_search(search_id):
    """Retrieve a saved search by ID"""
    db = DatabaseHelper()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM saved_searches WHERE id = ?', (search_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    # Reconstruct adopter profile
    adopter_profile = {
        'experience_level': row[3],
        'has_kids': bool(row[4]),
        'kid_ages': json.loads(row[5]),
        'has_other_pets': bool(row[6]),
        'other_pet_types': json.loads(row[7]),
        'home_type': row[8],
        'yard_size': row[9],
        'daily_exercise_minutes': row[10],
        'work_schedule': row[11],
        'allergies': row[12],
        'noise_tolerance': row[13],
        'training_commitment': row[14]
    }
    
    filters = {
        'species': row[15],
        'age': row[16],
        'size': row[17],
        'gender': row[18],
        'max_distance': row[19]
    }
    
    return {
        'id': row[0],
        'email': row[1],
        'name': row[2],
        'adopter_profile': adopter_profile,
        'filters': filters,
        'last_notified': row[20],
        'created_at': row[21],
        'active': bool(row[22])
    }


def get_all_active_searches():
    """Get all active saved searches"""
    db = DatabaseHelper()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM saved_searches WHERE active = 1')
    rows = cursor.fetchall()
    conn.close()
    
    searches = []
    for row in rows:
        search = get_saved_search(row[0])
        if search:
            searches.append(search)
    
    return searches


def update_last_notified(search_id):
    """Update the last notification timestamp"""
    db = DatabaseHelper()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'UPDATE saved_searches SET last_notified = ? WHERE id = ?',
        (datetime.now(), search_id)
    )
    
    conn.commit()
    conn.close()


def delete_saved_search(search_id):
    """Delete a saved search"""
    db = DatabaseHelper()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM saved_searches WHERE id = ?', (search_id,))
    
    conn.commit()
    conn.close()


if __name__ == "__main__":
    from src.adopter_profile import create_adopter_profile
    
    # Test saving a search
    test_profile = create_adopter_profile(
        experience_level='some_experience',
        home_type='house',
        daily_exercise_minutes=60
    )
    
    test_filters = {
        'species': 'Dog',
        'age': 'Young',
        'size': 'Medium'
    }
    
    search_id = save_search(
        email='test@example.com',
        name='My ideal dog search',
        adopter_profile=test_profile,
        filters=test_filters
    )
    
    print(f"✅ Saved search with ID: {search_id}")
    
    # Retrieve it
    retrieved = get_saved_search(search_id)
    print(f"✅ Retrieved search: {retrieved['name']}")
    print(f"   Email: {retrieved['email']}")
    print(f"   Filters: {retrieved['filters']}")
