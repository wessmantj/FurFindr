"""
Minimal CSS styling for FurFindr
Uses Streamlit's default dark mode - no color overrides
"""

import streamlit as st


def inject_custom_css():
    """Inject minimal custom CSS for consistent image sizing"""
    st.markdown("""
    <style>
        /* Fix image sizing to be square */
        img {
            width: 400px !important;
            height: 400px !important;
            object-fit: cover;
            border-radius: 8px;
        }
        
        /* Remove extra spacing */
        .block-container {
            padding-top: 2rem;
        }
        
        /* Ensure consistent button sizing */
        .stButton button {
            height: 2.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
