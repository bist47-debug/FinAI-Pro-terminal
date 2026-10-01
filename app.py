import streamlit as st
import os
from summarizer import extract_text_from_pdf, generate_earnings_brief, generate_multi_quarter_comparison
from streamlit_extras.colored_header import colored_header
from streamlit_extras.card import card
from streamlit_extras.add_vertical_space import add_vertical_space

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FinAI Pro | Institutional Earnings Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- API KEY INITIALIZATION ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# --- SIDEBAR CONFIGURATION ---
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

# --- HEADER SECTION ---
colored_header(
    label="📈 FinAI Pro Institutional Earnings Terminal",
    description="Next-generation NSE/BSE corporate filing intelligence, automated multi-quarter trend cross-examinations, and institutional document parsing.",
    color_name="blue-70"
)

add_vertical_space(1)

# --- SERVICE CARDS GRID USING STREAMLIT-EXTRAS ---
st.subheader("🚀 Core Intelligence Services")
col1, col2, col3 = st.columns(3)

with col1:
    card(
        title="📄 Single Filing Scan",
        text="Deep-dive extraction of quarterly earnings, revenue metrics, and EBITDA breakdowns from any PDF.",
        image="",
        url="",
        styles={
            "card": {
                "background-color": "#161b22",
                "border": "1px solid #30363d",
                "border-radius": "10px",
                "padding": "20px",
                "color": "#e6edf3"
            },
            "title": {"font-size": "18px", "color": "#ffffff"},
            "text": {"font-size": "14px", "color": "#8b949e"}
        }
    )

with col2:
    card(
        title="📊 Multi-Quarter Trend",
        text="Cross-examine multiple sequential reports to evaluate margin trajectories and YoY performance shifts.",
        image="",
        url="",
        styles={
            "card": {
                "background-color": "#161b22",
                "border": "1px solid #30363d",
                "border-radius": "10px",
                "padding": "20px",
                "color": "#e6edf3"
            },
            "title": {"font-size": "18px", "color": "#ffffff"},
            "text": {"font-size": "14px", "color": "#8b949e"}
        }
    )

with col3:
    card(
        title="⚡ Sample Sandbox",
        text="Test the terminal instantly using pre-loaded structural layouts before uploading your own reports.",
        image="",
        url="",
        styles={
            "card": {
                "background-color": "#161b22",
                "border": "1px solid #30363d",
                "border-radius": "10px",
                "padding": "20px",
                "color": "#e6edf3"
            },
            "title": {"font-size": "18px", "color": "#ffffff"},
            "text": {"font-size": "14px", "color": "#8b949e"}
        }
    )

add_vertical_space(2)

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
