
import streamlit as st
import os
from summarizer import extract_text_from_pdf, generate_earnings_brief, generate_multi_quarter_comparison

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FinAI Pro | Institutional Earnings Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PROFESSIONAL STYLING (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 2rem 1rem 3rem 1rem;
        background: linear-gradient(180deg, #161b22 0%, #0e1117 100%);
        border-bottom: 1px solid #30363d;
        margin-bottom: 2rem;
        border-radius: 12px;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #8b949e;
        max-width: 700px;
        margin: 0 auto;
    }

    /* Service Cards */
    .service-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 24px;
        border-radius: 10px;
        height: 100%;
        transition: border-color 0.2s;
    }
    .service-card:hover {
        border-color: #58a6ff;
    }
    .service-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    .service-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .service-desc {
        font-size: 0.9rem;
        color: #8b949e;
    }

    /* Custom Buttons */
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2ea043;
    }
    </style>
""", unsafe_allow_html=True)

# --- API KEY INITIALIZATION ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# --- SIDEBAR AUTH & CONFIG ---
st.sidebar.markdown("### ⚡ FinAI Pro Terminal")
st.sidebar.caption("NSE/BSE Corporate Intelligence")
st.sidebar.markdown("---")
auth_status = st.sidebar.selectbox("Access Mode", ["Guest View", "Admin / Institutional"])
if auth_status == "Admin / Institutional":
    pwd = st.sidebar.text_input("Admin Password", type="password")
    if pwd == "password123":
        st.sidebar.success("Pro Tier Unlocked")

st.sidebar.markdown("---")
analyst_name = st.sidebar.text_input("Analyst Watermark", value="Institutional Research Desk")

# --- HERO HEADER SECTION ---
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">📈 FinAI Pro Terminal</div>
        <div class="hero-subtitle">Next-generation NSE/BSE corporate filing intelligence, automated multi-quarter trend cross-examinations, and institutional document parsing.</div>
    </div>
""", unsafe_allow_html=True)

# --- SERVICE CARDS GRID ---
st.markdown("### 🚀 Core Intelligence Services")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="service-card">
            <div class="service-icon">📄</div>
            <div class="service-title">Single Filing Scan</div>
            <div class="service-desc">Deep-dive extraction of quarterly earnings, revenue metrics, EBITDA breakdowns, and risk factors from any PDF.</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="service-card">
            <div class="service-icon">📊</div>
            <div class="service-title">Multi-Quarter Trend</div>
            <div class="service-desc">Cross-examine multiple sequential reports to evaluate margin trajectories and YoY performance shifts.</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="service-card">
            <div class="service-icon">⚡</div>
            <div class="service-title">Sample Sandbox</div>
            <div class="service-desc">Test the terminal instantly using pre-loaded structural layouts before uploading your own reports.</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- WORKSPACE TABS ---
tab1, tab2, tab3 = st.tabs(["📄 Live Filing Workspace", "📊 Trend Analysis", "⚡ Sample Sandbox & Demo"])

with tab1:
    st.subheader("Upload & Analyze Corporate Filing")
    uploaded_file = st.file_uploader("Upload Quarterly Earnings PDF (NSE/BSE)", type=["pdf"], key="live_upload")
    
    if uploaded_file is not None:
        with st.spinner("Parsing document..."):
            pdf_text = extract_text_from_pdf(uploaded_file)
            if pdf_text and st.button("Generate Executive Brief"):
                with st.spinner("Running AI financial breakdown..."):
                    brief = generate_earnings_brief(pdf_text)
                    st.markdown(f"### 📋 Executive Briefing ({analyst_name})")
                    st.markdown(brief)

with tab2:
    st.subheader("Multi-Quarter Cross-Examination")
    uploaded_files = st.file_uploader("Upload 2+ Quarterly PDFs", type=["pdf"], accept_multiple_files=True, key="multi_upload")
    if uploaded_files and len(uploaded_files) >= 2:
        if st.button("Run Multi-Quarter Analysis"):
            with st.spinner("Analyzing trajectory..."):
                all_texts = [extract_text_from_pdf(f) for f in uploaded_files]
                comparison = generate_multi_quarter_comparison(all_texts)
                st.markdown("### 📊 Trajectory Report")
                st.markdown(comparison)

with tab3:
    st.subheader("Quick Sample Sandbox Scan")
    st.write("Want to see how the terminal processes documents instantly? Load a built-in mock sample preview:")
    
    if st.button("Run Basic Scan on Sample Data"):
        sample_mock_text = """
        XYZ Corp Q4 FY26 Financial Results. 
        Revenue reached INR 1,450 Crores, up 18% YoY. 
        EBITDA margins expanded by 220 basis points to 24.5% due to optimized supply chains. 
        Management guidance for FY27 projects 15-20% top-line growth.
        """
        with st.spinner("Scanning sample data..."):
            sample_brief = generate_earnings_brief(sample_mock_text)
            st.success("Sample scan completed successfully!")
            st.markdown(f"### 📋 Sample Executive Brief ({analyst_name})")
            st.markdown(sample_brief)
