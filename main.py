from fastapi import FastAPI, Body
import json
import threading
import time

from gemini_client import generate_multimodal, generate_text
from pydantic_models import AnalyzeRequest, PlanRequest, GenerateRequest
from action_models import ActionPlan
from prompts import ANALYZE_PROMPT, ACTION_PROMPT
from services.repo_graph_route import router as graph_router
from services.dependency_graph import analyze_repo
from intent_detector import detect_intent
from command_router import execute_command
from command_validator import validate_command

# from browser_loop import run_crawler
from repo_analyzer import repo_analyzer 

from google.cloud import firestore


app = FastAPI()
app.include_router(graph_router)

db = firestore.Client()


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


# ---------- HELPER : CHECK IF REPO ALREADY ANALYZED ----------
def repo_exists(repo_id):

    doc = db.collection("repo_analysis").document(repo_id).get()

    return doc.exists


# ---------- HELPER : START CRAWLER ----------
def start_crawler(owner, repo):

    print("Starting crawler for:", owner, repo)

    repo_analyzer(owner, repo)


# ---------- DAY 11 : COMMAND API ----------
@app.post("/command")
def command_api(data: dict = Body(...)):

    owner = data.get("owner")
    repo = data.get("repo")
    user_query = data.get("query") or data.get("command")

    if not user_query:
        return {"error": "No command provided"}

    repo_id = f"{owner}_{repo}"

    print("User query:", user_query)
    print("Repo:", repo_id)

    # ---------- START CRAWLER IF NEEDED ----------
    if not repo_exists(repo_id):

        print("Repo not analyzed yet. Starting crawler...")

        threading.Thread(
            target=repo_analyzer,
            args=(owner, repo),
            daemon=True
        ).start()

        return {
            "status": "analysis_started",
            "message": "Repository analysis started. Please wait a few minutes.",
            "repo_id": repo_id
        }

    # ---------- DETECT INTENT ----------
    intent = detect_intent(user_query)

    command = intent.get("command")
    confidence = intent.get("confidence")

    print("Detected command:", command)

    # ---------- VALIDATE COMMAND ----------
    if not validate_command(command):

        return {
            "error": "Unsupported command",
            "supported_commands": [
                "simulate_scaling",
                "explain_risk",
                "analyze_dependencies",
                "show_architecture"
            ],
            "confidence": confidence
        }

    # ---------- EXECUTE COMMAND ----------
    result = execute_command(command, repo_id)

    return {
    "repo_id": repo_id,
    "command_executed": command,
    "result": result,
    "confidence": confidence
    }