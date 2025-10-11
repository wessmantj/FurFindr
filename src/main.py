from dotenv import load_dotenv
load_dotenv()  # Load .env file

from src.api_client import PetfinderClient

def main():
    print("Testing Petfinder API connection...")
    
    # Create client (will automatically get token)
    try:
        client = PetfinderClient()
        print("✅ Successfully authenticated with Petfinder!")
        
        # Fetch 5 animals near NYC as a test
        print("\nFetching sample animals...")
        results = client.get_animals(location="02703", limit=5)
        
        animals = results.get('animals', [])
        print(f"✅ Found {len(animals)} animals\n")
        
        # Print details of each animal
        for animal in animals:
            print(f"- {animal['name']} ({animal['species']}) - {animal.get('age', 'Unknown age')}")
            print(f"  Breed: {animal.get('breeds', {}).get('primary', 'Unknown')}")
            print(f"  Status: {animal['status']}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
