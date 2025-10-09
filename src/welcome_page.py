"""
Professional Welcome/Launch Page for FurFindr
Clean, neutral design focused on credibility and simplicity
"""

import streamlit as st


def show_welcome_page():
    """Display professional welcome page for new users"""
    
    # Custom CSS for professional styling
    st.markdown("""
    <style>
        /* Global welcome page styling */
        .welcome-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Hero Section */
        .hero-section {
            text-align: center;
            padding: 80px 20px 60px 20px;
            background: var(--background-color);
            border-bottom: 1px solid var(--border-color);
        }
        
        .logo-text {
            font-size: 3.5rem;
            font-weight: 700;
            color: var(--text-color);
            letter-spacing: -1px;
            margin-bottom: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        .logo-accent {
            color: var(--secondary-text-color);
        }
        
        .tagline {
            font-size: 1.5rem;
            color: var(--text-color);
            font-weight: 400;
            margin-bottom: 40px;
            line-height: 1.6;
            opacity: 0.9;
        }
        
        .hero-description {
            font-size: 1.1rem;
            color: var(--secondary-text-color);
            max-width: 700px;
            margin: 0 auto 40px auto;
            line-height: 1.8;
        }
        
        /* Feature Grid */
        .features-section {
            padding: 60px 20px;
            background: var(--background-color);
        }
        
        .section-title {
            font-size: 2rem;
            font-weight: 600;
            color: var(--text-color);
            text-align: center;
            margin-bottom: 50px;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .feature-card {
            background: var(--secondary-background-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 35px 30px;
            transition: all 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        .feature-card:hover {
            border-color: var(--border-hover-color);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        .feature-number {
            display: inline-block;
            width: 40px;
            height: 40px;
            background: var(--background-color);
            border: 2px solid var(--border-color);
            border-radius: 50%;
            text-align: center;
            line-height: 36px;
            font-weight: 600;
            color: var(--text-color);
            margin-bottom: 20px;
            font-size: 1.1rem;
        }
        
        .feature-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-color);
            margin-bottom: 12px;
        }
        
        .feature-description {
            font-size: 1rem;
            color: var(--secondary-text-color);
            line-height: 1.7;
            flex-grow: 1;
        }
        
        /* Benefits Section */
        .benefits-section {
            padding: 60px 20px;
            background: var(--secondary-background-color);
            border-top: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
        }
        
        .benefit-item {
            display: flex;
            align-items: flex-start;
            margin-bottom: 25px;
            padding: 20px;
            background: var(--background-color);
            border-radius: 6px;
            border-left: 3px solid var(--accent-color);
        }
        
        .benefit-icon {
            font-size: 1.5rem;
            margin-right: 20px;
            color: var(--text-color);
            min-width: 30px;
        }
        
        .benefit-content {
            flex: 1;
        }
        
        .benefit-title {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-color);
            margin-bottom: 6px;
        }
        
        .benefit-text {
            font-size: 0.95rem;
            color: var(--secondary-text-color);
            line-height: 1.6;
        }
        
        /* Stats Section */
        .stats-section {
            padding: 50px 20px;
            text-align: center;
            background: var(--background-color);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 40px;
            max-width: 900px;
            margin: 0 auto;
        }
        
        .stat-item {
            padding: 20px;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-color);
            margin-bottom: 8px;
        }
        
        .stat-label {
            font-size: 0.95rem;
            color: var(--secondary-text-color);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 500;
        }
        
        /* CTA Section */
        .cta-section {
            padding: 60px 20px;
            text-align: center;
            background: var(--background-color);
        }
        
        .cta-title {
            font-size: 1.8rem;
            font-weight: 600;
            color: var(--text-color);
            margin-bottom: 20px;
        }
        
        .cta-subtitle {
            font-size: 1.1rem;
            color: var(--secondary-text-color);
            margin-bottom: 35px;
        }
        
        /* Disclaimer */
        .disclaimer-section {
            padding: 40px 20px;
            background: var(--secondary-background-color);
            border-top: 1px solid var(--border-color);
        }
        
        .disclaimer-box {
            max-width: 800px;
            margin: 0 auto;
            padding: 25px 30px;
            background: var(--background-color);
            border: 1px solid var(--border-color);
            border-radius: 6px;
        }
        
        .disclaimer-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-color);
            margin-bottom: 15px;
        }
        
        .disclaimer-text {
            font-size: 0.9rem;
            color: var(--secondary-text-color);
            line-height: 1.7;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Inject CSS variables based on current theme
    st.markdown("""
    <style>
        :root {
            --text-color: #2d3748;
            --secondary-text-color: #718096;
            --background-color: #ffffff;
            --secondary-background-color: #f8f9fa;
            --border-color: #e2e8f0;
            --border-hover-color: #cbd5e0;
            --accent-color: #a0aec0;
        }
        
        @media (prefers-color-scheme: dark) {
            :root {
                --text-color: #e2e8f0;
                --secondary-text-color: #a0aec0;
                --background-color: #1a202c;
                --secondary-background-color: #2d3748;
                --border-color: #4a5568;
                --border-hover-color: #718096;
                --accent-color: #718096;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="welcome-container">
        <div class="hero-section">
            <div class="logo-text">Fur<span class="logo-accent">Findr</span></div>
            <div class="tagline">Find compatible pets based on your lifestyle</div>
            <div class="hero-description">
                A data-driven platform that matches you with adoptable pets using 
                research-backed compatibility assessments, helping ensure successful, 
                long-term adoptions.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Get database stats
    try:
        from src.db_helper import DatabaseHelper
        db_helper = DatabaseHelper()
        pet_count = db_helper.get_animal_count()
    except:
        pet_count = "Loading..."
    
    # Stats Section
    st.markdown(f"""
    <div class="stats-section">
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-number">{pet_count}</div>
                <div class="stat-label">Available Pets</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">10+</div>
                <div class="stat-label">Risk Factors</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">Smart</div>
                <div class="stat-label">Matching System</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # How It Works Section
    st.markdown("""
    <div class="features-section">
        <div class="section-title">How It Works</div>
        <div class="feature-grid">
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">1</div>
            <div class="feature-title">Create Profile</div>
            <div class="feature-description">
                Share information about your household, experience level, and lifestyle preferences.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">2</div>
            <div class="feature-title">Browse Matches</div>
            <div class="feature-description">
                View adoptable pets sorted by compatibility with detailed risk assessments.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">3</div>
            <div class="feature-title">Review Guidance</div>
            <div class="feature-description">
                Understand potential challenges and receive detailed actionable recommendations.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-number">4</div>
            <div class="feature-title">Save Favorites</div>
            <div class="feature-description">
                Build a shortlist of matches and download comprehensive compatibility reports.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Benefits Section
    st.markdown("""
    <div class="benefits-section">
        <div class="section-title">Why Use FurFindr</div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="benefit-item">
            <div class="benefit-icon">✓</div>
            <div class="benefit-content">
                <div class="benefit-title">Research-Backed Assessment</div>
                <div class="benefit-text">
                    Our compatibility algorithm is built on peer-reviewed adoption research 
                    and documented shelter data patterns.
                </div>
            </div>
        </div>
        
        <div class="benefit-item">
            <div class="benefit-icon">✓</div>
            <div class="benefit-content">
                <div class="benefit-title">Identify Challenges Early</div>
                <div class="benefit-text">
                    Understand potential friction points before adoption, allowing you 
                    to prepare and seek appropriate resources.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="benefit-item">
            <div class="benefit-icon">✓</div>
            <div class="benefit-content">
                <div class="benefit-title">Transparent Scoring</div>
                <div class="benefit-text">
                    Every compatibility score includes detailed explanations and 
                    clear reasoning behind each assessment.
                </div>
            </div>
        </div>
        
        <div class="benefit-item">
            <div class="benefit-icon">✓</div>
            <div class="benefit-content">
                <div class="benefit-title">Actionable Guidance</div>
                <div class="benefit-text">
                    Receive specific recommendations and resources to address 
                    identified challenges and support successful adoption.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div class="cta-section">
        <div class="cta-title">Ready to Find Your Perfect Match?</div>
        <div class="cta-subtitle">
            Create your profile to get started with personalized pet recommendations.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started", type="primary", use_container_width=True):
            st.session_state.tutorial_completed = True
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Disclaimer Section
    st.markdown("""
    <div class="disclaimer-section">
        <div class="disclaimer-box">
            <div class="disclaimer-title">Important Information</div>
            <div class="disclaimer-text">
                FurFindr's compatibility assessments are guidance tools based on research 
                and data patterns. They do not guarantee specific pet behavior or outcomes. 
                Every animal is unique, and we strongly recommend meeting pets in person 
                and consulting with shelter staff before making adoption decisions. Risk 
                scores identify potential challenges to help you prepare, not to discourage 
                adoption. Your profile data remains private and is not shared with third parties.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
