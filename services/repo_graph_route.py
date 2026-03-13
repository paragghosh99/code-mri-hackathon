from fastapi import APIRouter
from services.scaling_simulator import run_scaling_simulation
from services.ai_explainer import explain_scaling
from services.dependency_graph import analyze_repo

router = APIRouter()

@router.get("/repo-graph/{repo_id}")
def repo_graph(repo_id: str):

    result = analyze_repo(repo_id)

    return result