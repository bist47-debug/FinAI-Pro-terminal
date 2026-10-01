import os
from pypdf import PdfReader
from openai import OpenAI

def extract_text_from_pdf(pdf_file_path):
    """Extracts raw text from an uploaded corporate filing PDF using pypdf."""
    reader = PdfReader(pdf_file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def generate_earnings_brief(pdf_text, api_key):
    """Sends financial text to OpenAI and returns a structured 1-page investment brief tailored for NSE/BSE reports."""
    client = OpenAI(api_key=api_key)
    
    prompt = f"""
    You are an expert equity research analyst specializing in Indian capital markets (NSE/BSE). Analyze the following corporate earnings/financial document and generate a clean, structured executive investment brief. Include:
    1. **Executive Summary & Financial Performance:** Revenue growth, EBITDA, Net Profit (Standalone vs Consolidated if applicable).
    2. **Key Operating Margins & Profitability:** Margin expansion/compression drivers.
    3. **Balance Sheet & Debt Health:** Leverage, working capital, and cash flow standing.
    4. **Management Commentary & Forward Guidance:** Strategic outlook, capex plans, and demand environment.
    
    Document Text:
    {pdf_text[:15000]}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    return response.choices[0].message.content

def generate_multi_quarter_comparison(text_q1, text_q2, api_key):
    """Compares two sequential filings (e.g., QoQ or YoY) to highlight trajectory and structural shifts."""
    client = OpenAI(api_key=api_key)
    
    prompt = f"""
    You are a senior quantitative equity analyst. Compare the following two consecutive corporate reports (Report A: Previous Period vs Report B: Latest Period) and provide a rigorous comparative breakdown focusing on:
    1. **Revenue & Margin Trajectory:** QoQ growth and margin changes.
    2. **Balance Sheet & Debt Delta:** Shifts in borrowings, liquidity, or capital allocation.
    3. **Management Tone & Guidance Shifts:** Did sentiment turn bullish, cautious, or defensive? Any changes in guidance?
    4. **Emerging Risks:** New risk factors or headwinds introduced in the latest filing.
    
    --- REPORT A (Previous Period) ---
    {text_q1[:10000]}
    
    --- REPORT B (Latest Period) ---
    {text_q2[:10000]}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    return response.choices[0].message.content
