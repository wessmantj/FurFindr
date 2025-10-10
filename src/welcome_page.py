"""
Clean professional welcome page for FurFindr
Single flowing design, no separate boxes
"""

import streamlit as st


def show_welcome_page():
    """Display clean professional welcome page"""
    
    # Hero section - clean and simple
    st.markdown("# FurFindr")
    st.markdown("### Find compatible pets based on your lifestyle")
    
    st.markdown("")
    st.markdown("A data-driven platform that matches you with adoptable pets using research-backed compatibility assessments.")
    
    # Get database count for stats
    try:
        from src.db_helper import DatabaseHelper
        db_helper = DatabaseHelper()
        pet_count = db_helper.get_animal_count()
    except:
        pet_count = "Loading..."
    
    st.markdown("---")
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Available Pets", pet_count)
    with col2:
        st.metric("Risk Factors Analyzed", "10+")
    with col3:
        st.metric("Smart Matching", "✓")
    
    st.markdown("---")
    
    # How it works - simple list, no boxes
    st.markdown("### How FurFindr Works")
    st.markdown("")
    
    st.markdown("**1. Create Your Profile**")
    st.markdown("Share information about your household, experience level, and lifestyle preferences.")
    st.markdown("")
    
    st.markdown("**2. Browse Matches**")
    st.markdown("View adoptable pets sorted by compatibility with detailed risk assessments.")
    st.markdown("")
    
    st.markdown("**3. Review Guidance**")
    st.markdown("Understand potential challenges and receive detailed actionable recommendations.")
    st.markdown("")
    
    st.markdown("**4. Save Favorites**")
    st.markdown("Build a shortlist of matches and download comprehensive compatibility reports.")
    
    st.markdown("---")
    
    # Why use section
    st.markdown("### Why Use FurFindr")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Research-Backed Assessment**")
        st.markdown("Our compatibility algorithm is built on peer-reviewed adoption research and documented shelter data patterns.")
        st.markdown("")
        
        st.markdown("**Identify Challenges Early**")
        st.markdown("Understand potential friction points before adoption, allowing you to prepare and seek appropriate resources.")
    
    with col2:
        st.markdown("**Transparent Scoring**")
        st.markdown("Every compatibility score includes detailed explanations and clear reasoning behind each assessment.")
        st.markdown("")
        
        st.markdown("**Actionable Guidance**")
        st.markdown("Receive specific recommendations and resources to address identified challenges and support successful adoption.")
    
    st.markdown("---")
    
    # CTA
    st.markdown("### Ready to Find Your Perfect Match?")
    st.markdown("Create your profile to get started with personalized pet recommendations.")
    st.markdown("")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started", type="primary", use_container_width=True):
            st.session_state.tutorial_completed = True
            st.rerun()
    
    st.markdown("")
    
    # Disclaimer
    with st.expander("Important Information"):
        st.markdown("""
        **About Risk Assessments**
        
        FurFindr's compatibility assessments are guidance tools based on research and data patterns. They do not guarantee specific pet behavior or outcomes. Every animal is unique, and we strongly recommend meeting pets in person and consulting with shelter staff before making adoption decisions. Risk scores identify potential challenges to help you prepare, not to discourage adoption.
        
        **Privacy**
        
        Your profile data remains private and is not shared with third parties.
        """)
