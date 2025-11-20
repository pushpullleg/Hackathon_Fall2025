"""
Main App - Integrates all pages with navigation
Run this to see the full flow: streamlit run app/main_app.py
"""
import streamlit as st
import sys
import os
import base64

# Add pages and components directories to path
base_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(base_dir, "pages"))
sys.path.insert(0, os.path.join(base_dir, "components"))

def load_profile_image_base64():
    """Load Mukesh profile image once per session."""
    if "profile_img_b64" in st.session_state:
        return st.session_state.profile_img_b64
    image_path = os.path.join(os.path.dirname(base_dir), "assets", "Muki_US_Photo.png")
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            st.session_state.profile_img_b64 = base64.b64encode(f.read()).decode()
            return st.session_state.profile_img_b64
    return None

# Page configuration
st.set_page_config(
    page_title="Renaissance - Adaptive Learning AI Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"

if "subject" not in st.session_state:
    st.session_state.subject = None

if "selected_path" not in st.session_state:
    st.session_state.selected_path = None

if "user_id" not in st.session_state:
    # Simple user id for analytics; single demo user for now
    st.session_state.user_id = "demo-mukesh"

if "show_ai_tutor" not in st.session_state:
    st.session_state.show_ai_tutor = False
if "show_analytics" not in st.session_state:
    st.session_state.show_analytics = False

# Navigation function
def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# Import page modules
from landing import (
    load_renaissance_theme as landing_theme,
    render_logo,
    render_tagline,
    render_hero_text,
    render_features,
    render_mission,
    render_footer
)

from onboarding import (
    load_renaissance_theme as onboarding_theme,
    render_small_logo as render_r_logo,
    render_question,
    render_progress as render_progress_onboarding
)

from roadmap_selection import (
    load_renaissance_theme as roadmap_theme,
    render_logo as render_roadmap_logo,
    render_page_title,
    render_roadmaps_side_by_side,
    render_progress as render_progress_roadmap
)

from data_engineer_roadmap import (
    load_renaissance_theme as de_roadmap_theme,
    render_logo as render_de_logo,
    render_page_header,
    render_roadmap
)

from ai_tutor_de import render_ai_tutor_panel
from analytics_de import render_de_analytics_panel

# Page: Landing
if st.session_state.current_page == "landing":
    landing_theme()
    render_logo()
    render_tagline()
    render_hero_text()
    
    # Custom Get Started button with navigation
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started", use_container_width=True, key="get_started_main"):
            navigate_to("onboarding")
    
    render_features()
    render_mission()
    render_footer()

# Page: Onboarding
elif st.session_state.current_page == "onboarding":
    onboarding_theme()
    render_r_logo()
    render_question()
    
    # Choice buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        cols = st.columns(2)
        
        with cols[0]:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 0.5rem;">
                <div style="font-size: 3rem; font-weight: 700; color: #CF3A4E; letter-spacing: 0.1em;">MKT</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Marketing", key="marketing_main", use_container_width=True):
                st.session_state.subject = "Marketing"
                st.success("✓ Marketing selected!")
                st.info("Dashboard coming soon...")
        
        with cols[1]:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 0.5rem;">
                <div style="font-size: 3rem; font-weight: 700; color: #CF3A4E; letter-spacing: 0.1em;">BUSA</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Business Analytics", key="analytics_main", use_container_width=True):
                st.session_state.subject = "Business Analytics"
                navigate_to("roadmap_selection")
    
    render_progress_onboarding()

# Page: Roadmap Selection
elif st.session_state.current_page == "roadmap_selection":
    roadmap_theme()
    render_roadmap_logo()
    render_page_title()
    
    # Render roadmaps with navigation
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<h3 class="category-title" style="color: #CF3A4E; font-size: 1.2rem; font-weight: 600; margin-bottom: 0.75rem; text-align: center;">Role-based Roadmaps</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([0.5, 2, 0.5])
        with col2:
            if st.button("Data Engineer", key="data_engineer_main", use_container_width=True):
                st.session_state.selected_path = "Data Engineer"
                navigate_to("data_engineer_roadmap")
            
            if st.button("Business Analyst", key="business_analyst_main", use_container_width=True):
                st.info("Coming soon!")
            
            if st.button("Financial Analyst", key="financial_analyst_main", use_container_width=True):
                st.info("Coming soon!")
    
    with col_right:
        st.markdown('<h3 class="category-title" style="color: #CF3A4E; font-size: 1.2rem; font-weight: 600; margin-bottom: 0.75rem; text-align: center;">Skill-based Roadmaps</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([0.5, 2, 0.5])
        with col2:
            if st.button("SQL", key="sql_main", use_container_width=True):
                st.info("Coming soon!")
            
            if st.button("AWS Cloud", key="aws_main", use_container_width=True):
                st.info("Coming soon!")
            
            if st.button("Power BI", key="powerbi_main", use_container_width=True):
                st.info("Coming soon!")
    
    render_progress_roadmap()

# Page: Data Engineer Roadmap
elif st.session_state.current_page == "data_engineer_roadmap":
    de_roadmap_theme()
    
    # Professional Navigation Bar - Single Row
    profile_img_b64 = load_profile_image_base64()
    profile_visual = (
        f'<img src="data:image/png;base64,{profile_img_b64}" '
        'style="width: 45px; height: 45px; border-radius: 50%; object-fit: cover; '
        'border: 3px solid #CF3A4E; box-shadow: 0 4px 12px rgba(207, 58, 78, 0.4);" alt="Mukesh">'
        if profile_img_b64
        else '<div class="profile-img">M</div>'
    )
    nav_html = """
    <style>
    /* Compact navigation bar */
    .nav-header {
        background-color: #000000;
        border-bottom: 2px solid #CF3A4E;
        padding: 0.75rem 1.5rem 2rem 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: -1rem -1rem 1rem -1rem;
        position: relative;
        min-height: 90px;
    }
    .profile-section {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .profile-img {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: linear-gradient(135deg, #CF3A4E, #A82E3E);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 1.3rem;
        border: 3px solid #CF3A4E;
        box-shadow: 0 4px 12px rgba(207, 58, 78, 0.4);
    }
    .profile-name {
        color: #FFFFFF;
        font-weight: 600;
        font-size: 1.05rem;
    }
    .title-section {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        text-align: center;
        width: auto;
    }
    .page-title {
        color: #FFFFFF;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
        white-space: nowrap;
    }
    .page-subtitle {
        color: #CF3A4E;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0.2rem 0 0 0;
        white-space: nowrap;
    }
    /* Button container styling */
    div[data-testid="column"] {
        display: flex;
        gap: 0.5rem;
        justify-content: flex-end;
    }
    </style>
    
    <div class="nav-header">
        <div class="profile-section">
            __PROFILE__
            <span class="profile-name">Mukesh</span>
        </div>
        <div class="title-section">
            <h1 class="page-title">Data Engineer Roadmap</h1>
            <p class="page-subtitle">Complete Learning Path</p>
        </div>
    </div>
    """
    st.markdown(nav_html.replace("__PROFILE__", profile_visual), unsafe_allow_html=True)
    
    # Action buttons - Analytics left, AI Tutor right
    btn_col1, btn_col2, btn_col3 = st.columns([2, 6, 2])
    
    with btn_col1:
        if st.button("📊 Learning Analytics", key="analytics_nav_btn", use_container_width=True):
            st.session_state.show_analytics = not st.session_state.show_analytics
            if st.session_state.show_analytics:
                st.session_state.show_ai_tutor = False
    
    with btn_col3:
        if st.button("🤖 Adaptive AI Tutor", key="ai_tutor_nav_btn", use_container_width=True):
            # Toggle the AI Tutor page view
            st.session_state.show_ai_tutor = not st.session_state.show_ai_tutor
            if st.session_state.show_ai_tutor:
                st.session_state.show_analytics = False
    
    st.markdown("---")
    
    # Either show roadmap, analytics, or AI Tutor page
    if st.session_state.show_ai_tutor:
        # Full-width tutor, with back button handled inside the panel
        render_ai_tutor_panel(
            user_name="Mukesh",
            user_id=st.session_state.user_id,
        )
    elif st.session_state.show_analytics:
        render_de_analytics_panel(
            user_id=st.session_state.user_id,
            user_name="Mukesh",
        )
    else:
        render_roadmap()

