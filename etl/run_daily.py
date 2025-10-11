import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()  # Load .env file before importing PetfinderClient

from src.api_client import PetfinderClient
from src.db_helper import DatabaseHelper

import time

def fetch_and_store_animals(zip_codes, species_list=None, limit_per_query=100):
    """
    Fetch animals from Petfinder and store in database
    
    Args:
        zip_codes: List of zip codes to search
        species_list: List of species to fetch (e.g., ['dog', 'cat'])
        limit_per_query: Animals per API call (max 100)
    """
    client = PetfinderClient()
    db = DatabaseHelper()
    
    total_saved = 0
    
    for zip_code in zip_codes:
        print(f"\n{'='*60}")
        print(f"Fetching animals near {zip_code}...")
        print(f"{'='*60}")
        
        species_to_fetch = species_list if species_list else [None]
        
        for species in species_to_fetch:
            try:
                # Fetch animals
                result = client.get_animals(
                    location=zip_code,
                    animal_type=species,
                    limit=limit_per_query
                )
                
                animals = result.get('animals', [])
                print(f"✅ Found {len(animals)} {species or 'animals'}")
                
                # Process each animal
                for animal in animals:
                    # Save animal
                    db.upsert_animal(animal)
                    
                    # Save photos
                    photos = animal.get('photos', [])
                    if photos:
                        db.upsert_photos(animal['id'], photos)
                    
                    # Save organization
                    org_id = animal.get('organization_id')
                    if org_id:
                        try:
                            org_result = client.get_organization(org_id)
                            org = org_result.get('organization', {})
                            db.upsert_organization(org)
                        except:
                            pass  # Skip if org fetch fails
                    
                    total_saved += 1
                
                # Be nice to the API - small delay between requests
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error fetching {species} in {zip_code}: {e}")
    
    print(f"\n{'='*60}")
    print(f"✅ ETL Complete! Saved {total_saved} animals")
    print(f"📊 Total animals in database: {db.get_animal_count()}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    # Configure your search
    ZIP_CODES = ["02790", "02703", "02139"] 
    SPECIES = ["dog"]  # Focus on dogs for demo - more breed variety
    
    fetch_and_store_animals(ZIP_CODES, SPECIES, limit_per_query=50)
