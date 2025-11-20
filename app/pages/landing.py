"""
Page 1: Landing/Home Page
Minimalist dark theme landing page matching Renaissance design.
"""
import streamlit as st
import os
import base64

# Page configuration
st.set_page_config(
    page_title="Renaissance - Adaptive Learning AI Agent",
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

# Load Renaissance theme with dark background
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
        padding: 1rem 2rem;
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
    
    /* Logo styling - Big R, Renaissance text below, centered */
    .logo-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 1rem auto 0 auto;
        gap: 0;
    }
    
    .logo-r-container {
        margin-bottom: -1rem;
        line-height: 0;
    }
    
    .logo-text-container {
        margin-top: -1rem;
        line-height: 0;
    }
    
    /* Tagline styling - Red */
    .tagline {
        color: #CF3A4E;
        font-size: 1.3rem;
        font-weight: 600;
        text-align: center;
        margin: 0 0 1rem 0;
        line-height: 1.2;
    }
    
    /* Hero text */
    .hero-text {
        color: #FFFFFF;
        font-size: 1rem;
        text-align: center;
        line-height: 1.6;
        max-width: 800px;
        margin: 0.5rem auto 1rem auto;
    }
    
    /* Key Features section */
    .features-heading {
        color: #FFFFFF;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1rem 0 0.75rem 0;
        text-align: left;
    }
    
    /* Feature content - no boxes */
    .feature-content {
        color: #FFFFFF;
        padding: 0.5rem 0;
        line-height: 1.6;
    }
    
    .feature-title {
        color: #FFFFFF;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .feature-icon {
        width: 24px;
        height: 24px;
        object-fit: contain;
        flex-shrink: 0;
    }
    
    .feature-description {
        color: #CCCCCC;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Mission section */
    .mission-container {
        margin-top: 1rem;
    }
    
    .mission-label {
        color: #FFFFFF;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .mission-text {
        color: #CCCCCC;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .mission-separator {
        color: #FFFFFF;
        margin: 0 0.5rem;
    }
    
    /* Get Started Button */
    .stButton > button {
        background-color: #CF3A4E;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        max-width: 250px;
        margin: 0.5rem auto;
        display: block;
    }
    
    .stButton > button:hover {
        background-color: #A82E3E;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(207, 58, 78, 0.4);
    }
    
    /* Center content */
    .centered {
        text-align: center;
    }
    
    /* Footer styling */
    .footer-container {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #FFFFFF;
    }
    
    .footer-text {
        color: #CCCCCC;
        font-size: 0.75rem;
        text-align: center;
        line-height: 1.5;
        margin: 0.5rem 0;
    }
    
    .footer-separator {
        color: #FFFFFF;
        margin: 0 0.5rem;
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
        # Fallback if files not found
        return None, None

def load_image_as_base64(image_filename):
    """Load image and convert to base64 for embedding."""
    project_root = get_project_root()
    image_path = os.path.join(project_root, 'assets', image_filename)
    try:
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        return None

def render_logo():
    """Render big Renaissance logo - no box."""
    logo_svg, logotype_svg = load_logo_svg()
    
    if logo_svg and logotype_svg:
        # Clean and prepare SVG for embedding
        logo_svg_clean = logo_svg.replace('<?xml version="1.0" encoding="utf-8"?>', '').replace('<!-- Generator: Adobe Illustrator 27.0.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->', '').strip()
        logotype_svg_clean = logotype_svg.replace('<?xml version="1.0" encoding="utf-8"?>', '').replace('<!-- Generator: Adobe Illustrator 27.0.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->', '').strip()
        
        st.markdown(f"""
        <div class="logo-container">
            <div class="logo-r-container" style="display: flex; align-items: flex-end; justify-content: center; line-height: 0;">
                <div style="width: 200px; height: 200px; display: flex; align-items: flex-end;">
                    {logo_svg_clean.replace('viewBox="0 0 2160 2160"', 'viewBox="0 0 2160 2160" width="200" height="200" style="fill: #FFFFFF; display: block;"')}
                </div>
            </div>
            <div class="logo-text-container" style="display: flex; align-items: flex-start; justify-content: center; line-height: 0;">
                <div style="width: 300px; height: 90px; display: flex; align-items: flex-start;">
                    {logotype_svg_clean.replace('viewBox="0 0 3840 2160"', 'viewBox="0 0 3840 2160" width="300" height="90" style="fill: #FFFFFF; display: block;"')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback text logo
        st.markdown("""
        <div class="logo-container">
            <h1 style="color: #FFFFFF; font-size: 4rem; font-weight: 700; margin: 0;">Renaissance</h1>
        </div>
        """, unsafe_allow_html=True)

def render_tagline():
    """Render 'See Every Student.' tagline in red."""
    st.markdown('<p class="tagline">See Every Student.</p>', unsafe_allow_html=True)

def render_hero_text():
    """Render hero text."""
    st.markdown("""
    <div class="hero-text">
        Master Marketing and Business Analytics with adaptive AI. Personalized insights. Relevant content.
    </div>
    """, unsafe_allow_html=True)

def render_features():
    """Render Key Features section with images instead of emojis."""
    st.markdown('<h3 class="features-heading">Key Features</h3>', unsafe_allow_html=True)
    
    # Load feature images
    adaptive_img = load_image_as_base64('adaptive learning.png')
    rag_img = load_image_as_base64('RAG.png')
    analytics_img = load_image_as_base64('Analytics.png')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if adaptive_img:
            st.markdown(f"""
            <div class="feature-content">
                <div class="feature-title">
                    <img src="data:image/png;base64,{adaptive_img}" class="feature-icon" alt="Adaptive Learning" />
                    Adaptive Learning
                </div>
                <div class="feature-description">
                    Bayesian Knowledge Tracing models student mastery in real-time, adapting to each learner's pace and needs.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="feature-content">
                <div class="feature-title">🤖 Adaptive Learning</div>
                <div class="feature-description">
                    Bayesian Knowledge Tracing models student mastery in real-time, adapting to each learner's pace and needs.
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if rag_img:
            st.markdown(f"""
            <div class="feature-content">
                <div class="feature-title">
                    <img src="data:image/png;base64,{rag_img}" class="feature-icon" alt="RAG-Enhanced Content" />
                    RAG-Enhanced Content
                </div>
                <div class="feature-description">
                    Retrieves relevant study materials using semantic search to provide contextual learning support.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="feature-content">
                <div class="feature-title">📚 RAG-Enhanced Content</div>
                <div class="feature-description">
                    Retrieves relevant study materials using semantic search to provide contextual learning support.
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        if analytics_img:
            st.markdown(f"""
            <div class="feature-content">
                <div class="feature-title">
                    <img src="data:image/png;base64,{analytics_img}" class="feature-icon" alt="Learning Analytics" />
                    Learning Analytics
                </div>
                <div class="feature-description">
                    Visual dashboards showing progress, mastery, and personalized recommendations for next steps.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="feature-content">
                <div class="feature-title">📊 Learning Analytics</div>
                <div class="feature-description">
                    Visual dashboards showing progress, mastery, and personalized recommendations for next steps.
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_get_started_button():
    """Render Get Started button."""
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started", use_container_width=True):
            st.success("✓ Ready to start learning!")
            st.info("💡 For full navigation, run: `streamlit run app/main_app.py`")

def render_mission():
    """Render Mission section in one line."""
    st.markdown("""
    <div class="mission-container">
        <p style="color: #FFFFFF; font-size: 0.95rem; line-height: 1.6; margin: 0;">
            <span class="mission-label">Our Mission :</span>
            <span class="mission-text"> To accelerate learning for all children and adults of all ability levels and ethnic and social backgrounds worldwide.</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render footer with team credit."""
    st.markdown("""
    <div class="footer-container">
        <p class="footer-text">
            Built by Team ACM for the Hackathon Fall 2025<span class="footer-separator">|</span>Adaptive AI Learning Agent.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main page content
load_renaissance_theme()

# Big logo at top (no box)
render_logo()

# Tagline
render_tagline()

# Hero text
render_hero_text()

# Get Started button
render_get_started_button()

# Key Features (with content, no boxes)
render_features()

# Mission section at bottom
render_mission()

# Footer
render_footer()

