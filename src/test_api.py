from src.api_client import PetfinderClient
import json

def test_endpoints():
    client = PetfinderClient()
    
    # Test 1: Get all animal types
    print("=" * 50)
    print("TEST 1: Fetching animal types...")
    types_data = client.get_types()
    types = types_data.get('types', [])
    print(f"✅ Found {len(types)} animal types:")
    for t in types[:5]:  # Show first 5
        print(f"  - {t['name']}")
    
    # Test 2: Get breeds for dogs
    print("\n" + "=" * 50)
    print("TEST 2: Fetching dog breeds...")
    breeds_data = client.get_breeds('dog')
    breeds = breeds_data.get('breeds', [])
    print(f"✅ Found {len(breeds)} dog breeds:")
    for b in breeds[:10]:  # Show first 10
        print(f"  - {b['name']}")
    
    # Test 3: Get animals and their organizations
    print("\n" + "=" * 50)
    print("TEST 3: Fetching animals with org info...")
    animals_data = client.get_animals(location="10001", limit=3)
    animals = animals_data.get('animals', [])
    
    for animal in animals:
        print(f"\n🐾 {animal['name']} ({animal['species']})")
        print(f"   Age: {animal.get('age', 'Unknown')}")
        print(f"   Breed: {animal.get('breeds', {}).get('primary', 'Unknown')}")
        
        # Get organization details
        org_id = animal.get('organization_id')
        if org_id:
            org_data = client.get_organization(org_id)
            org = org_data.get('organization', {})
            print(f"   Shelter: {org.get('name', 'Unknown')}")
            print(f"   Location: {org.get('address', {}).get('city', '')}, {org.get('address', {}).get('state', '')}")
    
    print("\n" + "=" * 50)
    print("✅ All API endpoints working!")

if __name__ == "__main__":
    test_endpoints()
