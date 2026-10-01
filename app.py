
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
    /* Main background & fonts */
    .stApp {
        background-color: #0e1117;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Card Container Styling */
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    
    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #111418;
        border-right: 1px solid #30363d;
    }
    
    /* Custom Buttons */
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #2ea043;
    }
    </style>
""", unsafe_allow_html=True)

# --- API KEY INITIALIZATION ---
# Automatically pulls from Streamlit Cloud Secrets or environment
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# --- SIDEBAR NAVIGATION & AUTH ---
st.sidebar.markdown("### ⚡ FinAI Pro Terminal")
st.sidebar.caption("NSE/BSE Corporate Filing Intelligence")
st.sidebar.markdown("---")

# Secure Login Simulation
auth_status = st.sidebar.selectbox("Access Mode", ["Guest View", "Admin / Institutional"])

if auth_status == "Admin / Institutional":
    pwd = st.sidebar.text_input("Admin Password", type="password")
    if pwd != "password123" and pwd != "":
        st.sidebar.error("Invalid Credentials")
    elif pwd == "password123":
        st.sidebar.success("Authenticated (Pro Tier)")

st.sidebar.markdown("---")
st.sidebar.subheader("Analyst Watermark")
analyst_name = st.sidebar.text_input("Prepared By:", value="Institutional Research Desk")

# --- MAIN DASHBOARD INTERFACE ---
st.title("📈 NSE/BSE Institutional Earnings & Trend Terminal")
st.markdown("Transform single filings or cross-examine multi-quarter trends with custom institutional branding.")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📄 Single Filing Brief", "📊 Multi-Quarter Trend", "⚙️ Terminal Settings"])

with tab1:
    st.subheader("Single Document Summarization")
    uploaded_file = st.file_uploader("Upload Quarterly Earnings PDF (NSE/BSE)", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Extracting text and parsing financial statements..."):
            pdf_text = extract_text_from_pdf(uploaded_file)
            
            if pdf_text:
                st.success("Document parsed successfully!")
                if st.button("Generate Executive Earnings Brief"):
                    with st.spinner("Running GPT-4o-mini financial analysis..."):
                        brief = generate_earnings_brief(pdf_text)
                        
                        st.markdown("---")
                        st.markdown(f"### 📋 Executive Briefing")
                        st.markdown(f"*{analyst_name}*")
                        st.markdown(brief)
            else:
                st.error("Could not extract text from this PDF. Please check the file.")

with tab2:
    st.subheader("Multi-Quarter Trend Cross-Examination")
    st.info("Upload multiple sequential quarter PDFs to analyze margin trajectories and growth metrics over time.")
    
    uploaded_files = st.file_uploader("Upload 2 or more Quarterly PDFs", type=["pdf"], accept_multiple_files=True)
    
    if uploaded_files and len(uploaded_files) >= 2:
        if st.button("Run Multi-Quarter Comparative Analysis"):
            with st.spinner("Analyzing cross-quarter trends..."):
                all_texts = [extract_text_from_pdf(f) for f in uploaded_files]
                comparison_result = generate_multi_quarter_comparison(all_texts)
                
                st.markdown("---")
                st.markdown("### 📊 Multi-Quarter Trajectory Report")
                st.markdown(comparison_result)
    elif uploaded_files:
        st.warning("Please upload at least 2 quarterly reports for trend comparisons.")

with tab3:
    st.subheader("Terminal Configuration")
    st.write("Current API Connection Status:")
    if os.environ.get("OPENAI_API_KEY"):
        st.success("API Key Active & Configured via Cloud Secrets.")
    else:
        st.error("API Key Missing. Please configure it in Streamlit Cloud Secrets.")
