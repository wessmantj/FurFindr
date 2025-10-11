#!/usr/bin/env python3
"""
Clear all animal data from the database while keeping the structure intact
"""
import sqlite3
import os

def clear_database():
    """Clear all data from animals, photos, and organizations tables"""
    
    db_path = 'db/app.db'
    
    if not os.path.exists(db_path):
        print("❌ Database doesn't exist yet. Run db/init_db.py first.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Count current records
    cursor.execute('SELECT COUNT(*) FROM animals')
    animal_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM photos')
    photo_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM organizations')
    org_count = cursor.fetchone()[0]
    
    print("=" * 60)
    print("Current database contents:")
    print(f"  Animals: {animal_count}")
    print(f"  Photos: {photo_count}")
    print(f"  Organizations: {org_count}")
    print("=" * 60)
    
    # Confirm deletion
    confirm = input("\n⚠️  Delete all data? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Cancelled. No data was deleted.")
        return
    
    # Delete all data
    cursor.execute('DELETE FROM photos')
    cursor.execute('DELETE FROM animals')
    cursor.execute('DELETE FROM organizations')
    
    # Don't delete saved_searches - keep user preferences
    
    conn.commit()
    
    print("\n✅ Database cleared successfully!")
    print("   - All animals deleted")
    print("   - All photos deleted")
    print("   - All organizations deleted")
    print("   - Saved searches preserved")
    print("\nRun 'python etl/run_daily.py' to fetch fresh data.")
    
    conn.close()

if __name__ == "__main__":
    clear_database()
