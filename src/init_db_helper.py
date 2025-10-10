"""
Database initialization for FurFindr
Ensures database exists and is properly set up on startup
"""

import sqlite3
import os


def ensure_database_exists():
    """Initialize database if it doesn't exist"""
    # Create db folder if it doesn't exist
    os.makedirs('db', exist_ok=True)
    
    db_path = 'db/app.db'
    
    # Check if database file exists
    if not os.path.exists(db_path):
        print("Database not found. Initializing...")
        init_database()
    else:
        # Verify tables exist
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='animals'")
            if not cursor.fetchone():
                print("Database exists but tables missing. Initializing...")
                init_database()
            conn.close()
        except Exception as e:
            print(f"Database check failed: {e}. Reinitializing...")
            init_database()


def init_database():
    """Initialize SQLite database with required tables"""
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
    
    # Saved searches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            name TEXT,
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
            species TEXT,
            age TEXT,
            size TEXT,
            gender TEXT,
            max_distance INTEGER,
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
    ensure_database_exists()
