import sqlite3

def check_database():
    conn = sqlite3.connect('db/app.db')
    cursor = conn.cursor()
    
    # Count animals
    cursor.execute('SELECT COUNT(*) FROM animals')
    animal_count = cursor.fetchone()[0]
    
    # Count organizations
    cursor.execute('SELECT COUNT(*) FROM organizations')
    org_count = cursor.fetchone()[0]
    
    # Count photos
    cursor.execute('SELECT COUNT(*) FROM photos')
    photo_count = cursor.fetchone()[0]
    
    print(f"📊 Database Summary:")
    print(f"  Animals: {animal_count}")
    print(f"  Organizations: {org_count}")
    print(f"  Photos: {photo_count}")
    
    # Show sample animals
    print(f"\n🐾 Sample Animals:")
    cursor.execute('SELECT name, species, age, size FROM animals LIMIT 5')
    for row in cursor.fetchall():
        print(f"  - {row[0]} ({row[1]}, {row[2]}, {row[3]})")
    
    conn.close()

if __name__ == "__main__":
    check_database()
