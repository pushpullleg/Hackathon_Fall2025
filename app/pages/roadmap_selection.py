"""
Page 3: Roadmap Selection
Shows two categories: Role-based and Skill-based roadmaps.
Only for Business Analytics (BUSA) students.
"""
import streamlit as st
import os
import base64

# Page configuration
st.set_page_config(
    page_title="Renaissance - Choose Your Path",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to prevent scrolling
st.markdown("""
<style>
    .stApp {
        overflow: hidden;
    }
    .main {
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Load Renaissance theme
def load_renaissance_theme():
    """Load Renaissance.com design system CSS with dark theme."""
    st.markdown("""
    <style>
    /* Dark Theme - Minimalist Design */
    
    /* Main background - Black */
    .stApp {
        background-color: #000000;
        padding: 0;
    }
    
    .main {
        background-color: #000000;
        padding: 1.5rem 2rem;
    }
    
    /* Reduce default padding */
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
        max-width: 1200px;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typography */
    * {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    h1, h2, h3, h4, p {
        color: #FFFFFF;
    }
    
    /* Page title */
    .page-title {
        color: #FFFFFF;
        font-size: 1.75rem;
        font-weight: 600;
        text-align: center;
        margin: 0.75rem 0 0.5rem 0;
    }
    
    .page-subtitle {
        color: #CCCCCC;
        font-size: 0.95rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* Category sections */
    .category-section {
        margin-bottom: 1.5rem;
    }
    
    .category-title {
        color: #CF3A4E;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        text-align: center;
    }
    
    /* Roadmap cards */
    .roadmap-title {
        color: #FFFFFF;
        font-size: 1rem;
        font-weight: 600;
        margin: 0;
    }
    
    /* Custom buttons */
    .stButton > button {
        background-color: transparent;
        border: 2px solid #333333;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        width: 100%;
        min-height: 60px;
    }
    
    .stButton > button:hover {
        border-color: #CF3A4E;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(207, 58, 78, 0.3);
        background-color: #1A1A1A;
    }
    
    /* Progress indicator */
    .progress-indicator {
        text-align: center;
        color: #666666;
        font-size: 0.75rem;
        margin-top: 1rem;
    }
    
    .progress-dots {
        display: flex;
        gap: 0.5rem;
        justify-content: center;
        margin-top: 0.5rem;
    }
    
    .progress-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #333333;
    }
    
    .progress-dot.active {
        background-color: #CF3A4E;
    }
    </style>
    """, unsafe_allow_html=True)

def get_project_root():
    """Get the project root directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, '../..')

def load_logo_svg():
    """Load Renaissance logo SVG."""
    project_root = get_project_root()
    logo_path = os.path.join(project_root, 'assets', 'Renaissance_Symbol_Black.svg')
    logotype_path = os.path.join(project_root, 'assets', 'Renaissance_Logotype_Black.svg')
    
    try:
        with open(logo_path, 'r') as f:
            logo_svg = f.read()
        with open(logotype_path, 'r') as f:
            logotype_svg = f.read()
        return logo_svg, logotype_svg
    except Exception as e:
        return None, None

def render_logo():
    """Render R logo at top."""
    logo_svg, logotype_svg = load_logo_svg()
    
    if logo_svg:
        logo_svg_clean = logo_svg.replace('<?xml version="1.0" encoding="utf-8"?>', '').replace('<!-- Generator: Adobe Illustrator 27.0.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->', '').strip()
        
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 0.5rem;">
            <div style="width: 50px; height: 50px;">
                {logo_svg_clean.replace('viewBox="0 0 2160 2160"', 'viewBox="0 0 2160 2160" width="50" height="50" style="fill: #FFFFFF;"')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 0.5rem;">
            <h1 style="color: #FFFFFF; font-size: 1.5rem; font-weight: 700;">R</h1>
        </div>
        """, unsafe_allow_html=True)

def render_page_title():
    """Render page title."""
    st.markdown("""
    <div>
        <h1 class="page-title">Choose Your Learning Path</h1>
        <p class="page-subtitle">Business Analytics Roadmaps</p>
    </div>
    """, unsafe_allow_html=True)

def render_roadmaps_side_by_side():
    """Render both roadmap types side by side."""
    col_left, col_right = st.columns(2)
    
    # Left column: Role-based
    with col_left:
        st.markdown('<h3 class="category-title">Role-based Roadmaps</h3>', unsafe_allow_html=True)
        
        # Center buttons with max width
        col1, col2, col3 = st.columns([0.5, 2, 0.5])
        with col2:
            if st.button("Data Engineer", key="data_engineer", use_container_width=True):
                st.session_state.selected_path = "Data Engineer"
                # Note: Navigation handled in main_app
                st.success("✓ Data Engineer path selected!")
                st.info("Loading roadmap...")
            
            if st.button("Business Analyst", key="business_analyst", use_container_width=True):
                st.info("Coming soon!")
            
            if st.button("Financial Analyst", key="financial_analyst", use_container_width=True):
                st.info("Coming soon!")
    
    # Right column: Skill-based
    with col_right:
        st.markdown('<h3 class="category-title">Skill-based Roadmaps</h3>', unsafe_allow_html=True)
        
        # Center buttons with max width
        col1, col2, col3 = st.columns([0.5, 2, 0.5])
        with col2:
            if st.button("SQL", key="sql", use_container_width=True):
                st.info("Coming soon!")
            
            if st.button("AWS Cloud", key="aws", use_container_width=True):
                st.info("Coming soon!")
            
            if st.button("Power BI", key="powerbi", use_container_width=True):
                st.info("Coming soon!")

def render_progress():
    """Render progress indicator."""
    st.markdown("""
    <div class="progress-indicator">
        <p>Step 2 of 3</p>
        <div class="progress-dots">
            <div class="progress-dot active"></div>
            <div class="progress-dot active"></div>
            <div class="progress-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main page content
load_renaissance_theme()

# Logo
render_logo()

# Page title
render_page_title()

# Both roadmap types side by side
render_roadmaps_side_by_side()

# Progress indicator
render_progress()

