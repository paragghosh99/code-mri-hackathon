from gemini_client import generate_text
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str
    
@app.get("/health")
def health_check():
    return {"status": "ok"}
@app.post("/generate")
def generate(request: GenerateRequest):
    output = generate_text(request.prompt)
    return {"response": output}