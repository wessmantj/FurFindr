import sqlite3
from datetime import datetime

class DatabaseHelper:
    def __init__(self, db_path='db/app.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def upsert_animal(self, animal_data):
        """Insert or update an animal record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO animals 
            (id, name, type, species, breed, age, size, gender, status, 
             distance, description, organization_id, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            animal_data.get('id'),
            animal_data.get('name'),
            animal_data.get('type'),
            animal_data.get('species'),
            animal_data.get('breeds', {}).get('primary'),
            animal_data.get('age'),
            animal_data.get('size'),
            animal_data.get('gender'),
            animal_data.get('status'),
            animal_data.get('distance'),
            animal_data.get('description'),
            animal_data.get('organization_id'),
            animal_data.get('url')
        ))
        
        conn.commit()
        conn.close()
    
    def upsert_organization(self, org_data):
        """Insert or update an organization record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        address = org_data.get('address', {})
        contact = org_data.get('contact', {})
        
        cursor.execute('''
            INSERT OR REPLACE INTO organizations 
            (id, name, email, phone, address, city, state, postcode, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            org_data.get('id'),
            org_data.get('name'),
            contact.get('email'),
            contact.get('phone'),
            f"{address.get('address1', '')} {address.get('address2', '')}".strip(),
            address.get('city'),
            address.get('state'),
            address.get('postcode'),
            org_data.get('url')
        ))
        
        conn.commit()
        conn.close()
    
    def upsert_photos(self, animal_id, photos_list):
        """Insert photos for an animal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Delete existing photos for this animal
        cursor.execute('DELETE FROM photos WHERE animal_id = ?', (animal_id,))
        
        # Insert new photos
        for photo in photos_list:
            if photo.get('medium'):  # Only save if photo exists
                cursor.execute(
                    'INSERT INTO photos (animal_id, photo_url) VALUES (?, ?)',
                    (animal_id, photo['medium'])
                )
        
        conn.commit()
        conn.close()
    
    def get_animal_count(self):
        """Get total number of animals in database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM animals')
        count = cursor.fetchone()[0]
        conn.close()
        return count
