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
    
    def get_animals(self, location, animal_type=None, limit=20):
        """Fetch animals from Petfinder API"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {
            'location': location,
            'limit': limit
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
