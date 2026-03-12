from fastapi import FastAPI
import json
from gemini_client import generate_multimodal, generate_text
from pydantic_models import AnalyzeRequest, PlanRequest, GenerateRequest
from action_models import ActionPlan
from prompts import ANALYZE_PROMPT, ACTION_PROMPT
from services.repo_graph_route import router as graph_router
from services.dependency_graph import analyze_repo

app = FastAPI()
app.include_router(graph_router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/generate")
def generate(request: GenerateRequest):
    output = generate_text(request.prompt)
    return {"response": output}


# ---------- DAY 2 : REPOSITORY ANALYSIS ----------
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

            Visible files:
            {request.files}
            """

    result = generate_text(prompt)

    cleaned = result.replace("```json", "").replace("```", "").strip()

    try:
        action = ActionPlan(**json.loads(cleaned))
        return {"action_plan": action}
    except Exception:
        return {"error": "Invalid action plan generated"}
