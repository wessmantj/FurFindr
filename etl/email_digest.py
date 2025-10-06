"""
Email Digest Generator
Creates and sends personalized pet recommendation emails
"""

import sys
import os
# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from dotenv import load_dotenv

from src.saved_search_helper import get_all_active_searches, update_last_notified, get_saved_search
from src.risk_engine import calculate_risk
from src.db_helper import DatabaseHelper


load_dotenv()


def get_new_pets_since(saved_search, hours=24):
    """
    Get pets matching search criteria that were added since last notification
    
    Args:
        saved_search: Dict with search criteria
        hours: Look back this many hours (default 24)
    
    Returns:
        List of matching pets
    """
    db = DatabaseHelper()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Calculate cutoff time
    if saved_search['last_notified']:
        cutoff = saved_search['last_notified']
    else:
        cutoff = datetime.now() - timedelta(hours=hours)
    
    # Build query
    query = '''
        SELECT id, name, type, species, breed, age, size, gender, description, url
        FROM animals 
        WHERE created_at > ? AND status = 'adoptable'
    '''
    params = [cutoff]
    
    # Add filters
    filters = saved_search['filters']
    if filters.get('species') and filters['species'] != 'All':
        query += ' AND type = ?'
        params.append(filters['species'])
    
    if filters.get('age') and filters['age'] != 'All':
        query += ' AND age = ?'
        params.append(filters['age'])
    
    if filters.get('size') and filters['size'] != 'All':
        query += ' AND size = ?'
        params.append(filters['size'])
    
    if filters.get('gender') and filters['gender'] != 'All':
        query += ' AND gender = ?'
        params.append(filters['gender'])
    
    query += ' LIMIT 10'  # Max 10 pets per email
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    pets = []
    for row in rows:
        pets.append({
            'id': row[0],
            'name': row[1],
            'type': row[2],
            'species': row[3],
            'breed': row[4],
            'age': row[5],
            'size': row[6],
            'gender': row[7],
            'description': row[8],
            'url': row[9]
        })
    
    return pets


def generate_email_html(saved_search, pets):
    """Generate HTML email content with pet recommendations"""
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .pet-card {{ border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 20px 0; }}
            .risk-badge {{ display: inline-block; padding: 5px 10px; border-radius: 5px; font-weight: bold; color: white; }}
            .risk-low {{ background-color: #4CAF50; }}
            .risk-medium {{ background-color: #FF9800; }}
            .risk-high {{ background-color: #F44336; }}
            .guidance {{ background-color: #f9f9f9; padding: 10px; margin: 10px 0; border-left: 3px solid #4CAF50; }}
            .footer {{ text-align: center; color: #777; margin-top: 30px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🐾 New Pets Match Your Search!</h1>
            <p>Here are {len(pets)} new pet(s) for: {saved_search['name']}</p>
        </div>
        
        <div style="padding: 20px;">
    """
    
    adopter_profile = saved_search['adopter_profile']
    
    if not pets:
        html += """
            <p>No new pets match your search criteria yet. We'll keep looking and notify you when we find matches!</p>
        """
    else:
        for pet in pets:
            # Calculate risk
            risk_result = calculate_risk(adopter_profile, pet)
            
            risk_class = f"risk-{risk_result['risk_level'].lower()}"
            
            html += f"""
            <div class="pet-card">
                <h2>🐾 {pet['name']}</h2>
                <p><strong>Breed:</strong> {pet['breed']} | <strong>Age:</strong> {pet['age']} | <strong>Size:</strong> {pet['size']}</p>
                
                <div class="risk-badge {risk_class}">
                    {risk_result['risk_level']} Risk for Your Household
                </div>
                
                <p><strong>Compatibility Score:</strong> {100 - risk_result['risk_score']}/100</p>
                <p>{risk_result['summary']}</p>
            """
            
            if risk_result['triggered_rules']:
                html += "<div class='guidance'>"
                html += f"<h3>⚠️ {len(risk_result['triggered_rules'])} Thing(s) to Consider:</h3>"
                
                for rule in risk_result['triggered_rules'][:3]:  # Top 3 concerns
                    html += f"<p><strong>{rule['rule_name']}</strong><br>"
                    html += f"<em>{rule['concern']}</em><br>"
                    html += "<strong>What to do:</strong> " + rule['guidance'][0] + "</p>"
                
                html += "</div>"
            else:
                html += "<p style='color: green;'>✅ Great match! No major concerns identified.</p>"
            
            if pet.get('url'):
                html += f"<p><a href='{pet['url']}' style='color: #4CAF50; font-weight: bold;'>View {pet['name']} on Petfinder →</a></p>"
            
            html += "</div>"
    
    html += """
        </div>
        
        <div class="footer">
            <p>You're receiving this because you saved a search on FurFindr.</p>
            <p>To update your preferences or unsubscribe, visit the app.</p>
        </div>
    </body>
    </html>
    """
    
    return html


def send_email(to_email, subject, html_content):
    """
    Send email using SMTP (Gmail example)
    
    Set these environment variables in .env:
    EMAIL_SENDER=your_email@gmail.com
    EMAIL_PASSWORD=your_app_password
    """
    
    sender_email = os.getenv('EMAIL_SENDER')
    sender_password = os.getenv('EMAIL_PASSWORD')
    
    if not sender_email or not sender_password:
        print("⚠️  Email credentials not configured. Set EMAIL_SENDER and EMAIL_PASSWORD in .env")
        print(f"Would send to: {to_email}")
        print(f"Subject: {subject}")
        return False
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    
    # Attach HTML
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    try:
        # Send via Gmail SMTP
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        
        print(f"✅ Email sent to {to_email}")
        return True
    
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def process_all_saved_searches():
    """Main function to process all saved searches and send emails"""
    
    print("\n" + "="*60)
    print("PROCESSING SAVED SEARCHES FOR EMAIL ALERTS")
    print("="*60 + "\n")
    
    searches = get_all_active_searches()
    
    if not searches:
        print("No active saved searches found.")
        return
    
    print(f"Found {len(searches)} active search(es)\n")
    
    for search in searches:
        print(f"Processing: {search['name']} ({search['email']})")
        
        # Get new pets
        pets = get_new_pets_since(search, hours=24)
        print(f"  Found {len(pets)} new matching pet(s)")
        
        if pets or True:  # Send even if no pets (for testing; remove "or True" in production)
            # Generate email
            html = generate_email_html(search, pets)
            subject = f"🐾 {len(pets)} New Pet(s) Match Your Search: {search['name']}"
            
            # Send email
            success = send_email(search['email'], subject, html)
            
            if success:
                # Update last notified time
                update_last_notified(search['id'])
                print(f"  ✅ Email sent and timestamp updated\n")
            else:
                print(f"  ⚠️  Email not sent (check credentials)\n")
        else:
            print(f"  No new pets to report\n")
    
    print("="*60)
    print("✅ All searches processed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    process_all_saved_searches()
