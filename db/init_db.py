import sqlite3
import os

def init_database():
    """Initialize SQLite database with required tables"""
    
    # Create db folder if it doesn't exist
    os.makedirs('db', exist_ok=True)
    
    # Connect to database (creates file if doesn't exist)
    conn = sqlite3.connect('db/app.db')
    cursor = conn.cursor()
    
    # Animals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            species TEXT,
            breed TEXT,
            age TEXT,
            size TEXT,
            gender TEXT,
            status TEXT,
            distance REAL,
            description TEXT,
            organization_id TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Organizations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            postcode TEXT,
            url TEXT
        )
    ''')
    
    # Photos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            animal_id TEXT,
            photo_url TEXT,
            FOREIGN KEY (animal_id) REFERENCES animals(id)
        )
    ''')
    
    # Saved searches table (for Day 5)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            zip_code TEXT,
            species TEXT,
            age TEXT,
            size TEXT,
            distance INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON animals(type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_age ON animals(age)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_size ON animals(size)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON animals(status)')
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_database()
