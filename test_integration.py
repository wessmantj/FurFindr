"""
Quick test to verify the welcome page integration
Run this to check if imports work correctly
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.welcome_page import show_welcome_page
    print("✓ Successfully imported show_welcome_page from src.welcome_page")
    
    from src.db_helper import DatabaseHelper
    print("✓ Successfully imported DatabaseHelper")
    
    from src.risk_engine import calculate_risk
    print("✓ Successfully imported calculate_risk")
    
    from src.adopter_profile import create_adopter_profile
    print("✓ Successfully imported create_adopter_profile")
    
    print("\n✅ All imports successful! The integration should work.")
    print("\nTo run FurFindr:")
    print("  streamlit run app/main.py")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    print("\nPlease check that all files are in the correct location.")
