import streamlit as st
import os
from summarizer import extract_text_from_pdf, generate_earnings_brief, generate_multi_quarter_comparison

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FinAI Pro | Earnings Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- EARNINGSCALL.AI INSPIRED STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Top Navigation Bar style */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
        border-bottom: 1px solid #1f2937;
        margin-bottom: 2rem;
    }
    
    /* Demo Company Grid Cards */
    .stock-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 16px;
        border-radius: 8px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .stock-card:hover {
        border-color: #3b82f6;
        background-color: #1f2937;
    }
    
    /* Section Containers */
    .content-box {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 24px;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- API KEY INITIALIZATION ---
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# --- SIDEBAR CONTROLS ---
st.sidebar.markdown("### 📊 FinAI Terminal")
st.sidebar.caption("Institutional Earnings Intelligence")
st.sidebar.markdown("---")

nav_mode = st.sidebar.radio("Navigation", ["Explore Demo Stocks", "Custom Filing Upload", "Multi-Quarter Matrix"])

st.sidebar.markdown("---")
analyst_name = st.sidebar.text_input("Analyst Watermark", value="Institutional Research Desk")

# --- MAIN HEADER ---
st.markdown("### ⚡ AI Earnings Call Summaries & Insights")
st.markdown("Skip hours of reading transcripts. Get key takeaways, guidance, and financial metrics in minutes.")
st.markdown("---")

if nav_mode == "Explore Demo Stocks":
    st.subheader("🔥 Quick-Select Market Demos")
    st.write("Click or test a pre-loaded corporate filing to experience the earnings intelligence brief instantly:")
    
    # Grid of demo companies like EarningsCall.ai
    col1, col2, col3, col4, col5 = st.columns(5)
    
    selected_demo = None
    with col1:
        if st.button("🍎 AAPL (Apple)"):
            selected_demo = "Apple Inc. Q4 FY26 Earnings Transcript. Revenue: $94.9B up 6% YoY. Services revenue hit an all-time high of $24.2B. Gross margin: 46.2%. Guidance for next quarter projects solid iPhone demand expansion."
    with col2:
        if st.button("🔍 GOOG (Google)"):
            selected_demo = "Alphabet Inc. Q3 Earnings Transcript. Cloud revenue grew 35% YoY to $11.4B. Operating margins expanded to 32%. AI infrastructure investments driving strong enterprise demand."
    with col3:
        if st.button("⚡ TSLA (Tesla)"):
            selected_demo = "Tesla Inc. Q3 Financial Update. Total revenues rose 8% YoY to $25.18B. Energy storage deployment reached a record 6.9 kWh. Operating margin came in at 7.6%."
    with col4:
        if st.button("💻 MSFT (Microsoft)"):
            selected_demo = "Microsoft Corp Q1 Earnings. Intelligent Cloud revenue up 20% driven heavily by Azure and cloud AI services. Capital expenditures increased to support scaling data centers."
    with col5:
        if st.button("🛒 AMZN (Amazon)"):
            selected_demo = "Amazon.com Q3 Results. AWS revenue accelerated to 19% growth YoY. Operating income improved significantly due to regionalized fulfillment network efficiencies."

    if selected_demo:
        st.markdown("---")
        with st.spinner("Generating instant AI earnings breakdown..."):
            brief = generate_earnings_brief(selected_demo)
            st.markdown(f"### 📋 Executive Earnings Brief ({analyst_name})")
            st.markdown(brief)
    else:
        st.info("Select any of the demo stocks above to view its structured earnings intelligence breakdown.")

elif nav_mode == "Custom Filing Upload":
    st.subheader("📄 Custom Filing Workspace")
    uploaded_file = st.file_uploader("Upload your corporate PDF earnings report or transcript (NSE/BSE/Global)", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("Extracting text and running financial analysis..."):
            pdf_text = extract_text_from_pdf(uploaded_file)
            if pdf_text and st.button("Generate Earnings Breakdown"):
                with st.spinner("Analyzing document metrics and management tone..."):
                    brief = generate_earnings_brief(pdf_text)
                    st.markdown("---")
                    st.markdown(f"### 📋 Executive Briefing ({analyst_name})")
                    st.markdown(brief)

elif nav_mode == "Multi-Quarter Matrix":
    st.subheader("📊 Multi-Quarter Trend Comparison")
    st.write("Cross-examine multiple reports side-by-side to track long-term performance shifts.")
    
    uploaded_files = st.file_uploader("Upload 2 or more sequential PDFs", type=["pdf"], accept_multiple_files=True)
    if uploaded_files and len(uploaded_files) >= 2:
        if st.button("Run Multi-Quarter Cross-Examination"):
            with st.spinner("Cross-examining sequential performance metrics..."):
                all_texts = [extract_text_from_pdf(f) for f in uploaded_files]
                comparison = generate_multi_quarter_comparison(all_texts)
                st.markdown("---")
                st.markdown("### 📊 Trajectory & Peer Comparison Report")
                st.markdown(comparison)
    elif uploaded_files:
        st.warning("Please upload at least 2 files to run a cross-examination matrix.")
