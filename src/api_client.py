import requests
import os
from dotenv import load_dotenv

load_dotenv()

class PetfinderClient:
    def __init__(self):
        self.api_key = os.getenv('PETFINDER_API_KEY')
        self.api_secret = os.getenv('PETFINDER_API_SECRET')
        self.base_url = "https://api.petfinder.com/v2"
        self.token = self._get_token()
    
    def _get_token(self):
        """Get OAuth token from Petfinder API"""
        auth_url = f"{self.base_url}/oauth2/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        response = requests.post(auth_url, data=data)
        response.raise_for_status()
        return response.json()['access_token']
    
    def get_types(self):
        """Get all animal types (dog, cat, etc.)"""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.base_url}/types", headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_breeds(self, animal_type):
        """Get breeds for a specific animal type"""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(
            f"{self.base_url}/types/{animal_type}/breeds",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_animals(self, location, animal_type=None, limit=20, page=1):
        """Fetch animals from Petfinder API with pagination"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {
            'location': location,
            'limit': limit,
            'page': page
        }
        if animal_type:
            params['type'] = animal_type
        
        response = requests.get(
            f"{self.base_url}/animals",
            headers=headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def get_organization(self, org_id):
        """Get details for a specific organization"""
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(
            f"{self.base_url}/organizations/{org_id}",
            headers=headers
        )
        response.raise_for_status()
        return response.json()
