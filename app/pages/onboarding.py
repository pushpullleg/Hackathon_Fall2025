"""
Page 2: Onboarding - Subject Selection
Interactive page asking students to choose between Marketing or Business Analytics.
"""
import streamlit as st
import os
import base64

# Page configuration
st.set_page_config(
    page_title="Renaissance - Get Started",
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
        padding: 2rem;
    }
    
    /* Reduce default padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
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
    
    /* Question container */
    .question-container {
        text-align: center;
        margin: 2rem auto 1.5rem auto;
        max-width: 800px;
    }
    
    .question-title {
        color: #FFFFFF;
        font-size: 1.75rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        line-height: 1.3;
    }
    
    .question-subtitle {
        color: #CCCCCC;
        font-size: 1rem;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }
    
    /* Choice buttons container */
    .choices-container {
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        margin: 1.5rem auto;
        max-width: 900px;
    }
    
    /* Choice card */
    .choice-card {
        background-color: #1A1A1A;
        border: 2px solid #333333;
        border-radius: 12px;
        padding: 2rem 1.5rem;
        width: 350px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .choice-card:hover {
        border-color: #CF3A4E;
        transform: translateY(-8px);
        box-shadow: 0 8px 24px rgba(207, 58, 78, 0.3);
    }
    
    .choice-icon {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #CF3A4E;
        letter-spacing: 0.1em;
    }
    
    .choice-title {
        color: #FFFFFF;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    .choice-description {
        color: #CCCCCC;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Custom button styling */
    .stButton > button {
        background-color: transparent;
        border: 2px solid #333333;
        color: #FFFFFF;
        border-radius: 12px;
        padding: 2rem 1.5rem;
        font-weight: 600;
        font-size: 1.3rem;
        transition: all 0.3s ease;
        width: 100%;
        height: 180px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .stButton > button:hover {
        border-color: #CF3A4E;
        transform: translateY(-8px);
        box-shadow: 0 8px 24px rgba(207, 58, 78, 0.3);
        background-color: #1A1A1A;
    }
    
    .stButton > button:active {
        background-color: #CF3A4E;
        border-color: #CF3A4E;
    }
    
    /* Progress indicator */
    .progress-indicator {
        text-align: center;
        color: #666666;
        font-size: 0.8rem;
        margin-top: 1.5rem;
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
    
    # Read SVG files
    try:
        with open(logo_path, 'r') as f:
            logo_svg = f.read()
        with open(logotype_path, 'r') as f:
            logotype_svg = f.read()
        return logo_svg, logotype_svg
    except Exception as e:
        return None, None

def render_small_logo():
    """Render R logo at top."""
    logo_svg, logotype_svg = load_logo_svg()
    
    if logo_svg:
        # Clean and prepare SVG for embedding
        logo_svg_clean = logo_svg.replace('<?xml version="1.0" encoding="utf-8"?>', '').replace('<!-- Generator: Adobe Illustrator 27.0.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->', '').strip()
        
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 1rem;">
            <div style="width: 80px; height: 80px;">
                {logo_svg_clean.replace('viewBox="0 0 2160 2160"', 'viewBox="0 0 2160 2160" width="80" height="80" style="fill: #FFFFFF;"')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <h1 style="color: #FFFFFF; font-size: 2.5rem; font-weight: 700;">R</h1>
        </div>
        """, unsafe_allow_html=True)

def render_question():
    """Render the main question section."""
    st.markdown("""
    <div class="question-container">
        <h1 class="question-title">What would you like to master?</h1>
        <p class="question-subtitle">
            Choose your area of focus to get personalized learning recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_choice_buttons():
    """Render the two choice buttons."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        cols = st.columns(2)
        
        with cols[0]:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 0.5rem;">
                <div class="choice-icon">MKT</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Marketing", key="marketing", use_container_width=True):
                st.session_state.subject = "Marketing"
                st.success("✓ Marketing selected!")
                st.info("Redirecting to dashboard...")
        
        with cols[1]:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 0.5rem;">
                <div class="choice-icon">BUSA</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Business Analytics", key="analytics", use_container_width=True):
                st.session_state.subject = "Business Analytics"
                st.success("✓ Business Analytics selected!")
                st.info("Redirecting to dashboard...")

def render_progress():
    """Render progress indicator."""
    st.markdown("""
    <div class="progress-indicator">
        <p>Step 1 of 3</p>
        <div class="progress-dots">
            <div class="progress-dot active"></div>
            <div class="progress-dot"></div>
            <div class="progress-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main page content
load_renaissance_theme()

# Small logo at top
render_small_logo()

# Question section
render_question()

# Choice buttons
render_choice_buttons()

# Progress indicator
render_progress()

