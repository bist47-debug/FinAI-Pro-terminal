import streamlit as st
import os
from summarizer import extract_text_from_pdf, generate_earnings_brief, generate_multi_quarter_comparison

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="FinAI Pro — NSE/BSE Institutional Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN DESIGN SYSTEM & CUSTOM CSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #e6edf3;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: #111827;
        border: 1px solid #1f2937 !important;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #1f2937;
        padding: 16px;
        border-radius: 10px;
    }
    div[data-testid="stMetric"] label { color: #9ca3af !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #f3f4f6 !important; }
    
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1rem;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        border: none;
        color: white;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #030712;
        border-right: 1px solid #1f2937;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE MANAGEMENT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_subscribed" not in st.session_state:
    st.session_state.is_subscribed = False

# --- SIDEBAR NAVIGATION & AUTHENTICATION ---
with st.sidebar:
    st.markdown("### ⚡ FinAI Pro Terminal")
    st.markdown("<p style='color: #9ca3af; font-size: 0.85rem;'>NSE/BSE Corporate Filing Intelligence</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    if not st.session_state.logged_in:
        st.subheader("🔐 Secure Login")
        u_name = st.text_input("Username", placeholder="Enter username")
        u_pass = st.text_input("Password", type="password", placeholder="Enter password")
        if st.button("Authenticate", use_container_width=True):
            if u_name == "admin" and u_pass == "password123":
                st.session_state.logged_in = True
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Invalid credentials. (Hint: admin / password123)")
    else:
        st.success("🟢 Status: Authenticated")
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

        st.markdown("---")
        st.subheader("💳 Membership Tier")
        if st.session_state.is_subscribed:
            st.success("Pro Tier: Active ($29/mo)")
            st.markdown("<p style='font-size: 0.8rem; color: #9ca3af;'>Multi-quarter tracking & analyst branding enabled.</p>", unsafe_allow_html=True)
        else:
            st.warning("🔒 Free Tier (Locked)")
            if st.button("Upgrade via Stripe ($29/mo)", use_container_width=True):
                st.session_state.is_subscribed = True
                st.success("Payment Verified! Pro Unlocked.")
                st.rerun()

        st.markdown("---")
        st.subheader("🏷️ Analyst Branding")
        analyst_name = st.text_input("Firm / Analyst Watermark", "Your Name / Capital Research")

# --- MAIN DASHBOARD INTERFACE ---
st.title("📊 NSE/BSE Institutional Earnings & Trend Terminal")
st.markdown("Transform single filings or cross-examine multi-quarter trends with custom analyst branding.")
st.markdown("---")

if not st.session_state.logged_in:
    st.info("👈 Please enter your credentials in the sidebar to launch the workspace.")
elif not st.session_state.is_subscribed:
    st.error("🔒 **Pro Subscription Required:** Upgrade your account via the sidebar to unlock the document intelligence engine.")
else:
    # Navigation Tabs for Single vs Multi-Quarter Analysis
    tab1, tab2 = st.tabs(["📄 Single Report Summarizer", "📈 Multi-Quarter Trend Comparison"])
    
    with tab1:
        col1, col2 = st.columns([1.6, 1], gap="medium")
        with col1:
            with st.container(border=True):
                st.subheader("📥 Document Intake")
                ticker1 = st.text_input("Target Ticker Symbol", "RELIANCE.NS", key="t1")
                pdf_single = st.file_uploader("Upload Quarterly Report PDF (NSE/BSE)", type=["pdf"], key="p1")
                run_single = st.button("Generate Executive Brief", use_container_width=True, key="b1")
        with col2:
            with st.container(border=True):
                st.subheader("⚙️ Engine Status")
                st.metric(label="Inference Engine", value="GPT-4o Mini", delta="Optimized")
                st.metric(label="Parser Status", value="pypdf (v3.0+)", delta="Secure")

        if run_single:
            api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
            if not api_key:
                st.error("⚠️ OpenAI API key missing from Colab secrets.")
            elif pdf_single is not None:
                with st.spinner("Analyzing Indian market disclosures..."):
                    with open("temp_single.pdf", "wb") as f:
                        f.write(pdf_single.getbuffer())
                    text_data = extract_text_from_pdf("temp_single.pdf")
                    output = generate_earnings_brief(text_data, api_key)
                
                # Apply Analyst Branding to Output
                branded_output = f"**Prepared by:** {analyst_name}\n\n" + output

                st.markdown("---")
                st.success("✨ Analysis Generated Successfully!")
                with st.container(border=True):
                    st.markdown(f"### 📑 Executive Brief: {ticker1}")
                    st.markdown(branded_output)
                    st.download_button("📥 Export Branded Brief", data=branded_output, file_name=f"{ticker1}_Executive_Brief.txt", use_container_width=True, key="d1")
            else:
                st.warning("⚠️ Please upload a valid PDF file first.")

    with tab2:
        st.markdown("### 📈 Sequential Quarter-over-Quarter (QoQ) Analysis")
        st.markdown("Upload two consecutive NSE/BSE filings to trace margin adjustments, risk evolutions, and guidance deltas.")
        
        col_a, col_b = st.columns(2, gap="medium")
        with col_a:
            with st.container(border=True):
                st.subheader("Previous Period Report")
                pdf_prev = st.file_uploader("Upload Previous Quarter PDF", type=["pdf"], key="prev_pdf")
        with col_b:
            with st.container(border=True):
                st.subheader("Latest Period Report")
                pdf_latest = st.file_uploader("Upload Latest Quarter PDF", type=["pdf"], key="latest_pdf")
                
        ticker_comp = st.text_input("Company Ticker for Comparison", "RELIANCE.NS", key="comp_ticker")
        run_comparison = st.button("Run Multi-Quarter Comparative Analysis", use_container_width=True)

        if run_comparison:
            api_key = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
            if not api_key:
                st.error("⚠️ OpenAI API key missing from Colab secrets.")
            elif pdf_prev is not None and pdf_latest is not None:
                with st.spinner("Cross-examining financial deltas between quarters..."):
                    with open("temp_prev.pdf", "wb") as f:
                        f.write(pdf_prev.getbuffer())
                    with open("temp_latest.pdf", "wb") as f:
                        f.write(pdf_latest.getbuffer())
                    
                    text_prev = extract_text_from_pdf("temp_prev.pdf")
                    text_latest = extract_text_from_pdf("temp_latest.pdf")
                    
                    comparison_output = generate_multi_quarter_comparison(text_prev, text_latest, api_key)
                
                # Apply Analyst Branding to Output
                branded_comparison = f"**Prepared by:** {analyst_name}\n\n" + comparison_output

                st.markdown("---")
                st.success("✨ Comparative Intelligence Generated!")
                with st.container(border=True):
                    st.markdown(f"### 📊 QoQ Trend Report: {ticker_comp}")
                    st.markdown(branded_comparison)
                    st.download_button("📥 Export Branded Trend Report", data=branded_comparison, file_name=f"{ticker_comp}_QoQ_Comparison.txt", use_container_width=True, key="d2")
            else:
                st.warning("⚠️ Please upload both the previous and latest quarterly report PDFs to run the comparison.")
