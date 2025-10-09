"""
Professional styling for FurFindr main application
Consistent with welcome page design
"""

import streamlit as st


def inject_professional_css():
    """Inject professional CSS styling for the main app"""
    
    st.markdown("""
    <style>
        /* CSS Variables for theme consistency */
        :root {
            --text-color: #2d3748;
            --secondary-text-color: #718096;
            --background-color: #ffffff;
            --secondary-background-color: #f8f9fa;
            --border-color: #e2e8f0;
            --border-hover-color: #cbd5e0;
            --accent-color: #4a5568;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
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
        
        /* Lock sidebar - always visible */
        section[data-testid="stSidebar"] {
            position: sticky !important;
            top: 0 !important;
            height: 100vh !important;
        }
        
        section[data-testid="stSidebar"] > div {
            height: 100vh !important;
            overflow-y: auto !important;
        }
        
        /* Main app header styling */
        .main-header {
            text-align: center;
            padding: 40px 20px 30px 20px;
            background: var(--background-color);
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 30px;
        }
        
        .app-title {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-color);
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }
        
        .app-subtitle {
            font-size: 1.1rem;
            color: var(--secondary-text-color);
            font-weight: 400;
        }
        
        /* Professional pet card styling */
        .pet-card-container {
            background: var(--secondary-background-color);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: all 0.3s ease;
        }
        
        /* Pet photo styling */
        .pet-card-container img {
            border-radius: 8px;
            height: 300px;
            width: 100%;
            object-fit: cover;
            object-position: center;
        }
        
        .pet-card-container:hover {
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            transform: translateY(-2px);
        }
        
        .pet-name {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-color);
            margin: 0 0 10px 0;
        }
        
        .risk-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .risk-badge-low {
            background-color: var(--success-color);
            color: white;
        }
        
        .risk-badge-medium {
            background-color: var(--warning-color);
            color: white;
        }
        
        .risk-badge-high {
            background-color: var(--danger-color);
            color: white;
        }
        
        /* Metrics dashboard styling */
        .metrics-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-color);
            margin: 30px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--border-color);
        }
        
        /* Professional sidebar styling */
        .sidebar-section-header {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-color);
            margin: 20px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-color);
        }
        
        /* Button styling */
        .stButton > button {
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div {
            background-color: var(--accent-color);
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: var(--secondary-background-color);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-weight: 500;
        }
        
        /* Form styling */
        .stSelectbox label, .stSlider label, .stCheckbox label, .stMultiSelect label {
            font-weight: 500;
            color: var(--text-color);
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-color);
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.9rem;
            font-weight: 500;
            color: var(--secondary-text-color);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Remove Streamlit branding for cleaner look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Divider styling */
        hr {
            border: none;
            border-top: 1px solid var(--border-color);
            margin: 30px 0;
        }
    </style>
    """, unsafe_allow_html=True)


def render_app_header():
    """Render professional app header"""
    st.markdown("""
    <div class="main-header">
        <div class="app-title">Fur<span style="color: var(--secondary-text-color);">Findr</span></div>
        <div class="app-subtitle">Find compatible pets based on your lifestyle</div>
    </div>
    """, unsafe_allow_html=True)


def render_pet_card_header(pet_name, risk_level):
    """Render professional pet card header with name and risk badge"""
    
    risk_class = {
        'Low': 'risk-badge-low',
        'Medium': 'risk-badge-medium',
        'High': 'risk-badge-high'
    }.get(risk_level, 'risk-badge-medium')
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div class="pet-name">{pet_name}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="risk-badge {risk_class}">{risk_level} Risk</div>', unsafe_allow_html=True)


def render_metrics_header(title):
    """Render professional metrics section header"""
    st.markdown(f'<div class="metrics-header">{title}</div>', unsafe_allow_html=True)


def render_sidebar_section_header(title):
    """Render professional sidebar section header"""
    st.markdown(f'<div class="sidebar-section-header">{title}</div>', unsafe_allow_html=True)
