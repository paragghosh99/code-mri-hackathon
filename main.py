from fastapi import FastAPI
from gemini_client import generate_text, generate_multimodal
from pydantic import BaseModel
from prompts import ANALYZE_PROMPT, ACTION_PROMPT
from pydantic_models import AnalyzeRequest, GenerateRequest, PlanRequest
from action_models import Coordinates, ActionPlan
import json

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/generate")
def generate(request: GenerateRequest):
    output = generate_text(request.prompt)
    return {"response": output}


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    prompt = f"""
            {ANALYZE_PROMPT}

            Instruction:
            {request.instruction}
            """
    
    result = generate_multimodal(prompt, request.image_base64)

    return {"analysis": result}


# ---------- DAY 3 : ACTION PLANNING ----------
@app.post("/plan")
async def plan_action(request: PlanRequest):

    prompt = f"""
            {ACTION_PROMPT}

            Repository analysis:
            {request.analysis.model_dump()}
            """

    result = generate_text(prompt)

    cleaned = result.replace("```json", "").replace("```", "").strip()

    try:
        action = ActionPlan(**json.loads(cleaned))
        return {"action_plan": action}
    except Exception:
        return {"error": "Invalid action plan generated"}