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
    
    # Saved searches table (enhanced for Day 5)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            name TEXT,
            
            -- Adopter profile
            experience_level TEXT,
            has_kids INTEGER,
            kid_ages TEXT,
            has_other_pets INTEGER,
            other_pet_types TEXT,
            home_type TEXT,
            yard_size TEXT,
            daily_exercise_minutes INTEGER,
            work_schedule TEXT,
            allergies TEXT,
            noise_tolerance TEXT,
            training_commitment TEXT,
            
            -- Search filters
            species TEXT,
            age TEXT,
            size TEXT,
            gender TEXT,
            max_distance INTEGER,
            
            -- Tracking
            last_notified TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            active INTEGER DEFAULT 1
        )
    ''')
    
    # Create indexes for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON animals(type)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_age ON animals(age)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_size ON animals(size)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON animals(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_created ON animals(created_at)')
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    init_database()
