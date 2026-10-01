from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import io
import os
import openai

app = FastAPI(title="FinAI Pro API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze-filing")
async def analyze_filing(file: UploadFile = File(...)):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable is missing on the server.")
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")
    
    contents = await file.read()
    reader = PdfReader(io.BytesIO(contents))
    raw_text = "".join([page.extract_text() or "" for page in reader.pages])
    
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from PDF.")
    
    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "You are a senior institutional equity research analyst. Produce an executive brief covering Revenue metrics, EBITDA growth, management tone, and forward guidance."
            },
            {
                "role": "user", 
                "content": f"Analyze this corporate filing:\n\n{raw_text[:12000]}"
            }
        ],
        temperature=0.3
    )
    
    return {
        "status": "success",
        "filename": file.filename,
        "brief": response.choices[0].message.content
    }

@app.get("/api/health")
def health_check():
    return {"status": "online"}
