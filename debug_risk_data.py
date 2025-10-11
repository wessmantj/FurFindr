import sqlite3
import sys
sys.path.append('.')

from dotenv import load_dotenv
load_dotenv()

from src.risk_engine import calculate_risk, is_high_energy, is_working_herding_breed
from src.adopter_profile import SAMPLE_PROFILES

# Connect to database
conn = sqlite3.connect('db/app.db')
cursor = conn.cursor()

print("="*70)
print("DEBUGGING: Checking actual pet data vs risk engine expectations")
print("="*70)

# Get a sample of large dogs
query = """
SELECT id, name, breed, age, size, description 
FROM animals 
WHERE type = 'Dog' AND size IN ('Large', 'Extra Large', 'large', 'extra large', 'X-Large')
LIMIT 10
"""

cursor.execute(query)
rows = cursor.fetchall()

print(f"\n📊 Found {len(rows)} large dogs. Checking first few...\n")

# Use the high-risk profile
high_risk_profile = SAMPLE_PROFILES['high_risk']

print("Testing with HIGH RISK profile:")
print(f"  - First-time owner: {high_risk_profile['experience_level']}")
print(f"  - Has toddler: {high_risk_profile['has_kids']} ({high_risk_profile['kid_ages']})")
print(f"  - Apartment, no yard: {high_risk_profile['home_type']}, {high_risk_profile['yard_size']}")
print(f"  - Exercise time: {high_risk_profile['daily_exercise_minutes']} mins")
print(f"  - Work schedule: {high_risk_profile['work_schedule']}")
print(f"  - Training commitment: {high_risk_profile['training_commitment']}\n")

for row in rows:
    pet = {
        'id': row[0],
        'name': row[1],
        'breed': row[2] or 'Unknown',
        'age': row[3],
        'size': row[4],
        'description': row[5] or ''
    }
    
    print("="*70)
    print(f"🐕 {pet['name']}")
    print(f"   Breed: {pet['breed']}")
    print(f"   Age: '{pet['age']}' (type: {type(pet['age'])})")
    print(f"   Size: '{pet['size']}' (type: {type(pet['size'])})")
    print(f"   Description: {pet['description'][:100]}...")
    
    # Check what functions return
    print(f"\n   🔍 Function checks:")
    print(f"   - is_high_energy(): {is_high_energy(pet)}")
    print(f"   - is_working_herding_breed(): {is_working_herding_breed(pet)}")
    
    # Calculate risk
    result = calculate_risk(high_risk_profile, pet)
    
    print(f"\n   📊 Risk Result:")
    print(f"   - Risk Score: {result['risk_score']}")
    print(f"   - Risk Level: {result['risk_level']}")
    print(f"   - Rules Triggered: {len(result['triggered_rules'])}")
    
    if result['triggered_rules']:
        print(f"   - Triggered rules:")
        for rule in result['triggered_rules']:
            print(f"      • {rule['rule_name']} ({rule['weight']} pts)")
    else:
        print(f"   - ⚠️  NO RULES TRIGGERED!")
    
    print()

# Also check unique values in the database
print("\n" + "="*70)
print("DATABASE VALUE ANALYSIS")
print("="*70)

cursor.execute("SELECT DISTINCT age FROM animals WHERE age IS NOT NULL ORDER BY age")
ages = [row[0] for row in cursor.fetchall()]
print(f"\nUnique AGE values in database: {ages}")

cursor.execute("SELECT DISTINCT size FROM animals WHERE size IS NOT NULL ORDER BY size")
sizes = [row[0] for row in cursor.fetchall()]
print(f"Unique SIZE values in database: {sizes}")

cursor.execute("SELECT DISTINCT species FROM animals WHERE species IS NOT NULL")
species = [row[0] for row in cursor.fetchall()]
print(f"Unique SPECIES values: {species}")

# Check breeds that should match
print(f"\n" + "="*70)
print("BREED MATCHING TEST")
print(f"="*70)

cursor.execute("""
    SELECT breed, COUNT(*) as count 
    FROM animals 
    WHERE breed IS NOT NULL 
    GROUP BY breed 
    ORDER BY count DESC 
    LIMIT 20
""")
breed_counts = cursor.fetchall()

print("\nTop 20 breeds in database:")
for breed, count in breed_counts:
    print(f"  - {breed}: {count}")

conn.close()

print("\n" + "="*70)
print("EXPECTED VALUES BY RISK ENGINE:")
print("="*70)
print("Ages: ['Baby', 'Young', 'Adult', 'Senior']")
print("Sizes: ['Small', 'Medium', 'Large', 'Extra Large']")
print("\n⚠️  If your database values don't match these EXACTLY, rules won't trigger!")
print("="*70)
