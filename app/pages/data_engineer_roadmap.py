"""
Page 4: Data Engineer Roadmap
Displays the complete Data Engineer learning roadmap with all pillars and topics.
"""
import streamlit as st
import os
import base64
import sys

# Add components directory for tutor/analytics panels
components_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "components")
if components_path not in sys.path:
    sys.path.insert(0, components_path)

from ai_tutor_de import render_ai_tutor_panel
from analytics_de import render_de_analytics_panel

# Page configuration
st.set_page_config(
    page_title="Renaissance - Data Engineer Roadmap",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "show_ai_tutor" not in st.session_state:
    st.session_state.show_ai_tutor = False
if "show_analytics" not in st.session_state:
    st.session_state.show_analytics = False
if "user_id" not in st.session_state:
    st.session_state.user_id = "demo-mukesh"

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
        padding: 1rem 2rem;
        overflow-y: auto;
        height: 100vh;
    }
    
    /* Reduce default padding */
    .block-container {
        padding-top: 0.5rem;
        padding-bottom: 1rem;
        max-width: 1400px;
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
    
    /* Page header */
    .page-header {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .page-title {
        color: #FFFFFF;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .page-subtitle {
        color: #CF3A4E;
        font-size: 1rem;
        font-weight: 600;
    }
    
    /* Infographic Roadmap Container - Three Lane Layout */
    .roadmap-infographic {
        position: relative;
        max-width: 1600px;
        margin: 0 auto;
        padding: 2rem 0;
        display: grid;
        grid-template-columns: 1fr 500px 1fr;
        gap: 0;
    }
    
    /* Central vertical line - Bright and visible */
    .timeline-line {
        position: absolute;
        left: 50%;
        top: 0;
        bottom: 0;
        width: 5px;
        background: linear-gradient(to bottom, #00D9FF, #00A8E8, #0077B6);
        transform: translateX(-50%);
        z-index: 1;
        box-shadow: 0 0 10px rgba(0, 217, 255, 0.5);
    }
    
    /* Three lanes */
    .lane-left, .lane-center, .lane-right {
        position: relative;
        padding: 1rem;
    }
    
    .lane-center {
        z-index: 3;
    }
    
    /* Pillar section container */
    .pillar-section {
        display: contents;
    }
    
    /* Main pillar box (center lane, highlighted) */
    .main-pillar-box {
        background: linear-gradient(135deg, #FFD700 0%, #FFC700 100%);
        border: 4px solid #FFB700;
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin: 2rem 0;
        text-align: center;
        position: relative;
        z-index: 4;
        box-shadow: 0 8px 24px rgba(255, 215, 0, 0.5);
    }
    
    .main-pillar-title {
        color: #000000 !important;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Ensure all text inside yellow boxes is black */
    .main-pillar-box {
        color: #000000 !important;
    }
    
    .main-pillar-box * {
        color: #000000 !important;
    }
    
    /* Branch containers */
    .branch-left-container, .branch-right-container {
        display: flex;
        flex-direction: column;
        gap: 2rem;
        padding: 2rem 1rem;
    }
    
    /* Topic box (side lanes) - High contrast */
    .topic-box {
        background: linear-gradient(135deg, #2A2A2A 0%, #1A1A1A 100%);
        border: 3px solid #00D9FF;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        position: relative;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0, 217, 255, 0.3);
    }
    
    .topic-box:hover {
        border-color: #FFD700;
        transform: scale(1.02);
        box-shadow: 0 6px 24px rgba(255, 215, 0, 0.4);
    }
    
    .topic-box-title {
        color: #FFFFFF;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #00A8E8;
    }
    
    /* Item list inside topic boxes */
    .topic-items-list {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .item-chip {
        background-color: #333333;
        border: 2px solid #00A8E8;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        color: #FFFFFF;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .item-chip:hover {
        background-color: #00A8E8;
        border-color: #00D9FF;
        color: #000000;
        font-weight: 600;
    }
    
    /* Connection lines - Bright and visible */
    .dotted-line-left {
        position: absolute;
        border-top: 4px dotted #00D9FF;
        width: 80px;
        top: 30px;
        right: -80px;
        z-index: 2;
        filter: drop-shadow(0 0 3px rgba(0, 217, 255, 0.7));
    }
    
    .dotted-line-right {
        position: absolute;
        border-top: 4px dotted #00D9FF;
        width: 80px;
        top: 30px;
        left: -80px;
        z-index: 2;
        filter: drop-shadow(0 0 3px rgba(0, 217, 255, 0.7));
    }
    
    /* Single column layout for smaller screens */
    @media (max-width: 968px) {
        .topics-branches {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        .timeline-line {
            left: 20px;
        }
        .main-pillar-box {
            margin-left: 60px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def get_project_root():
    """Get the project root directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, '../..')

def load_profile_image_base64():
    """Load Mukesh profile photo from assets."""
    if "profile_img_b64" in st.session_state:
        return st.session_state.profile_img_b64
    project_root = get_project_root()
    image_path = os.path.join(project_root, "assets", "Muki_US_Photo.png")
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            st.session_state.profile_img_b64 = base64.b64encode(f.read()).decode()
            return st.session_state.profile_img_b64
    return None

def render_navigation_bar():
    """Render top navigation bar with profile and AI Tutor button."""
    # Initialize session state for modals
    if "show_analytics" not in st.session_state:
        st.session_state.show_analytics = False
    if "show_ai_tutor" not in st.session_state:
        st.session_state.show_ai_tutor = False
    
    # Load profile image
    profile_path = os.path.join(get_project_root(), "assets", "mukesh_profile.jpg")
    
    # Check if profile image exists, otherwise use placeholder
    if os.path.exists(profile_path):
        with open(profile_path, "rb") as f:
            profile_img_data = base64.b64encode(f.read()).decode()
        profile_img_src = f"data:image/jpeg;base64,{profile_img_data}"
    else:
        # Placeholder SVG for profile
        profile_img_src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='50' height='50'%3E%3Ccircle cx='25' cy='25' r='25' fill='%23CF3A4E'/%3E%3Ctext x='25' y='32' font-size='20' fill='white' text-anchor='middle' font-family='Arial'%3EM%3C/text%3E%3C/svg%3E"
    
    # CSS for navigation bar
    st.markdown("""
    <style>
    /* Navigation bar container */
    .nav-container {
        position: sticky;
        top: 0;
        background-color: #000000;
        border-bottom: 2px solid #CF3A4E;
        padding: 1rem 2rem;
        z-index: 1000;
        margin-bottom: 1rem;
    }
    
    /* Custom button styles for nav */
    .nav-container .stButton > button {
        width: auto;
        margin: 0;
    }
    
    /* Profile button styling */
    div[data-testid="column"]:first-child .stButton > button {
        background: transparent !important;
        border: 2px solid #CF3A4E !important;
        color: #FFFFFF !important;
        border-radius: 50px !important;
        padding: 0.5rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="column"]:first-child .stButton > button:hover {
        background: #CF3A4E !important;
        transform: scale(1.05) !important;
        box-shadow: 0 4px 12px rgba(207, 58, 78, 0.5) !important;
    }
    
    /* AI Tutor button styling */
    div[data-testid="column"]:last-child .stButton > button {
        background: linear-gradient(135deg, #00A8E8 0%, #0077B6 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(0, 168, 232, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="column"]:last-child .stButton > button:hover {
        background: linear-gradient(135deg, #00D9FF 0%, #00A8E8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(0, 217, 255, 0.5) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation bar container
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    # Create navigation layout with columns
    nav_cols = st.columns([1, 6, 1])
    
    with nav_cols[0]:
        # Profile button with image
        profile_html = f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
            <img src="{profile_img_src}" style="width: 40px; height: 40px; border-radius: 50%; border: 3px solid #CF3A4E; object-fit: cover; box-shadow: 0 4px 12px rgba(207, 58, 78, 0.4);" alt="Profile">
            <span style="color: #FFFFFF; font-size: 0.9rem; font-weight: 600;">Mukesh</span>
        </div>
        """
        st.markdown(profile_html, unsafe_allow_html=True)
        if st.button("📊 Learning Analytics", key="profile_btn", use_container_width=True):
            st.session_state.show_analytics = True
            st.rerun()
    
    with nav_cols[2]:
        # AI Tutor button
        if st.button("🤖 Adaptive AI Tutor", key="ai_tutor_btn", use_container_width=True):
            st.session_state.show_ai_tutor = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def load_logo_svg():
    """Load Renaissance logo SVG."""
    project_root = get_project_root()
    logo_path = os.path.join(project_root, 'assets', 'Renaissance_Symbol_Black.svg')
    
    try:
        with open(logo_path, 'r') as f:
            logo_svg = f.read()
        return logo_svg
    except Exception as e:
        return None

def render_logo():
    """Render small R logo at top."""
    logo_svg = load_logo_svg()
    
    if logo_svg:
        logo_svg_clean = logo_svg.replace('<?xml version="1.0" encoding="utf-8"?>', '').replace('<!-- Generator: Adobe Illustrator 27.0.1, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->', '').strip()
        
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-bottom: 0.5rem;">
            <div style="width: 40px; height: 40px;">
                {logo_svg_clean.replace('viewBox="0 0 2160 2160"', 'viewBox="0 0 2160 2160" width="40" height="40" style="fill: #FFFFFF;"')}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 0.5rem;">
            <h1 style="color: #FFFFFF; font-size: 1.5rem; font-weight: 700;">R</h1>
        </div>
        """, unsafe_allow_html=True)

def render_page_header():
    """Render page header."""
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">Data Engineer Roadmap</h1>
        <p class="page-subtitle">Complete Learning Path</p>
    </div>
    """, unsafe_allow_html=True)

def load_roadmap_data():
    """Load roadmap data from JSON."""
    roadmap_data = {
        "title": "Data Engineer Roadmap",
        "pillars": [
            {
                "id": "foundations",
                "name": "Foundations",
                "topics": [
                    {
                        "name": "Core Skills",
                        "items": [
                            "Python", "SQL", "Git & GitHub", "Linux Basics",
                            "Data Structures & Algorithms", "Networking Fundamentals",
                            "Distributed Systems Basics"
                        ]
                    }
                ]
            },
            {
                "id": "data_basics",
                "name": "Data Ecosystem Basics",
                "topics": [
                    {
                        "name": "Understanding Data",
                        "items": [
                            "Data Generation", "Sources: DBs, APIs, Logs, IoT",
                            "Data Lifecycle: Ingest, Store, Process, Serve"
                        ]
                    },
                    {
                        "name": "Modeling & Concepts",
                        "items": [
                            "Normalization", "Star Schema", "Snowflake Schema",
                            "Slowly Changing Dimensions", "OLTP vs OLAP",
                            "CAP Theorem", "Scaling: Horizontal vs Vertical"
                        ]
                    }
                ]
            },
            {
                "id": "storage",
                "name": "Storage & Databases",
                "topics": [
                    {
                        "name": "Relational Databases",
                        "items": ["MySQL", "PostgreSQL", "SQL Server", "MariaDB", "Oracle"]
                    },
                    {
                        "name": "NoSQL Databases",
                        "items": [
                            "Document: MongoDB, CouchDB", "Column: Cassandra, BigTable, HBase",
                            "Graph: Neo4j, Amazon Neptune", "Key-Value: Redis, DynamoDB"
                        ]
                    },
                    {
                        "name": "Warehouses & Lakes",
                        "items": [
                            "BigQuery", "Amazon Redshift", "Snowflake",
                            "S3 Data Lake", "Delta Lake", "Databricks"
                        ]
                    },
                    {
                        "name": "Modern Architectures",
                        "items": [
                            "Data Mesh", "Data Fabric",
                            "Metadata-First Architecture", "Serverless Data Platforms"
                        ]
                    }
                ]
            },
            {
                "id": "pipelines",
                "name": "Data Ingestion & Pipelines",
                "topics": [
                    {
                        "name": "Ingestion Types",
                        "items": [
                            "Batch Ingestion", "Streaming Ingestion",
                            "Real-Time Ingestion", "Hybrid Approaches"
                        ]
                    },
                    {
                        "name": "Pipeline Fundamentals",
                        "items": ["ETL & ELT", "Extract → Transform → Load"]
                    },
                    {
                        "name": "Pipeline Tools",
                        "items": ["Apache Airflow", "dbt", "Luigi", "Prefect"]
                    },
                    {
                        "name": "Messaging Systems",
                        "items": ["Apache Kafka", "RabbitMQ", "AWS SQS", "AWS SNS"]
                    }
                ]
            },
            {
                "id": "bigdata_infra",
                "name": "Big Data & Infrastructure",
                "topics": [
                    {
                        "name": "Hadoop Ecosystem",
                        "items": ["HDFS", "YARN", "MapReduce"]
                    },
                    {
                        "name": "Big Data Engines",
                        "items": ["Apache Spark"]
                    },
                    {
                        "name": "Containers & Cluster Management",
                        "items": ["Docker", "Kubernetes", "GKE", "EKS"]
                    },
                    {
                        "name": "Cloud Platforms",
                        "items": [
                            "AWS: EC2, S3, RDS, Glue",
                            "Azure: VMs, Blob Storage, Data Factory",
                            "GCP: Compute Engine, GCS, Dataflow"
                        ]
                    },
                    {
                        "name": "Infrastructure as Code",
                        "items": ["Terraform", "AWS CDK", "Google Deployment Manager", "OpenTofu"]
                    }
                ]
            },
            {
                "id": "serving_governance",
                "name": "Data Serving & Governance",
                "topics": [
                    {
                        "name": "Analytics & BI",
                        "items": ["Power BI", "Tableau", "Looker", "Streamlit"]
                    },
                    {
                        "name": "Reverse ETL",
                        "items": ["Hightouch", "Census", "Segment"]
                    },
                    {
                        "name": "Security",
                        "items": [
                            "Authentication vs Authorization", "Encryption",
                            "Tokenization", "Data Masking", "Data Obfuscation"
                        ]
                    },
                    {
                        "name": "Governance & Quality",
                        "items": [
                            "Data Lineage", "Metadata Management",
                            "Data Interoperability", "Data Quality Monitoring",
                            "Privacy Laws: GDPR, ECPA, EU AI Act"
                        ]
                    },
                    {
                        "name": "Testing",
                        "items": [
                            "Unit Testing", "Integration Testing", "End-to-End Testing",
                            "Load Testing", "A/B Testing", "Smoke Testing"
                        ]
                    }
                ]
            }
        ]
    }
    return roadmap_data

def render_pillar(pillar):
    """Render a single pillar in three-lane structure with branches."""
    topics = pillar['topics']
    
    # Split topics into left and right branches
    mid_point = (len(topics) + 1) // 2
    left_topics = topics[:mid_point]
    right_topics = topics[mid_point:]
    
    # Left lane with left branch topics
    left_html = '<div class="branch-left-container">'
    for topic in left_topics:
        left_html += '<div class="topic-box">'
        left_html += '<div class="dotted-line-left"></div>'
        left_html += f'<div class="topic-box-title">{topic["name"]}</div>'
        left_html += '<div class="topic-items-list">'
        for item in topic['items']:
            left_html += f'<div class="item-chip">{item}</div>'
        left_html += '</div></div>'
    left_html += '</div>'
    
    # Center lane with main pillar box
    center_html = f'<div class="main-pillar-box"><h3 class="main-pillar-title">{pillar["name"]}</h3></div>'
    
    # Right lane with right branch topics
    right_html = '<div class="branch-right-container">'
    for topic in right_topics:
        right_html += '<div class="topic-box">'
        right_html += '<div class="dotted-line-right"></div>'
        right_html += f'<div class="topic-box-title">{topic["name"]}</div>'
        right_html += '<div class="topic-items-list">'
        for item in topic['items']:
            right_html += f'<div class="item-chip">{item}</div>'
        right_html += '</div></div>'
    right_html += '</div>'
    
    # Render in three columns using Streamlit
    cols = st.columns([1, 1.2, 1])
    with cols[0]:
        st.markdown(left_html, unsafe_allow_html=True)
    with cols[1]:
        st.markdown(center_html, unsafe_allow_html=True)
    with cols[2]:
        st.markdown(right_html, unsafe_allow_html=True)

def render_roadmap():
    """Render the complete roadmap as an infographic with central timeline."""
    roadmap_data = load_roadmap_data()
    pillars = roadmap_data['pillars']
    
    # Container with timeline
    st.markdown('<div style="position: relative;">', unsafe_allow_html=True)
    
    # Central timeline - starts below the header (after "Complete Learning Path")
    st.markdown('''
    <div style="position: fixed; left: 50%; top: 200px; bottom: 0; width: 5px; 
                background: linear-gradient(to bottom, #00D9FF, #00A8E8, #0077B6); 
                transform: translateX(-50%); z-index: 0; 
                box-shadow: 0 0 10px rgba(0, 217, 255, 0.5);">
    </div>
    ''', unsafe_allow_html=True)
    
    # Render each pillar in three-lane structure
    for pillar in pillars:
        render_pillar(pillar)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main page content
load_renaissance_theme()

# Navigation bar at the very top
st.markdown("""
<style>
.nav-bar-simple {
    background-color: #000000;
    border-bottom: 2px solid #CF3A4E;
    padding: 1rem 2rem;
    margin: -1rem -1rem 1rem -1rem;
}
</style>
<div class="nav-bar-simple"></div>
""", unsafe_allow_html=True)

# Create navigation using columns
col1, col2, col3 = st.columns([2, 6, 2])

with col1:
    profile_img_b64 = load_profile_image_base64()
    if profile_img_b64:
        profile_markup = f"""
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <img src="data:image/png;base64,{profile_img_b64}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover; border: 2px solid #CF3A4E; box-shadow: 0 4px 12px rgba(207, 58, 78, 0.3);" alt="Mukesh">
            <span style="color: #FFFFFF; font-weight: 600;">Mukesh</span>
        </div>
        """
    else:
        profile_markup = """
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 40px; height: 40px; border-radius: 50%; background: #CF3A4E; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; border: 2px solid #CF3A4E;">M</div>
            <span style="color: #FFFFFF; font-weight: 600;">Mukesh</span>
        </div>
        """
    st.markdown(profile_markup, unsafe_allow_html=True)
    if st.button("📊 Learning Analytics", key="analytics_btn"):
        st.session_state.show_analytics = not st.session_state.show_analytics
        if st.session_state.show_analytics:
            st.session_state.show_ai_tutor = False

with col3:
    if st.button("🤖 Adaptive AI Tutor", key="tutor_btn"):
        st.session_state.show_ai_tutor = not st.session_state.show_ai_tutor
        if st.session_state.show_ai_tutor:
            st.session_state.show_analytics = False

st.markdown("---")

# Logo
render_logo()

# Page header
render_page_header()

if st.session_state.show_ai_tutor:
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
    # Roadmap content
    render_roadmap()

