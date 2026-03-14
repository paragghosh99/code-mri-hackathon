from fastapi import APIRouter
from services.scaling_simulator import run_scaling_simulation
from services.ai_explainer import explain_scaling
from services.dependency_graph import analyze_repo
import json
from pathlib import Path

CACHE_DIR = Path("ai_cache")
CACHE_DIR.mkdir(exist_ok=True)

def get_cached_ai(repo):
    file = CACHE_DIR / f"{repo}.json"

    if file.exists():
        with open(file) as f:
            return json.load(f)

    return None


def save_cached_ai(repo, data):
    file = CACHE_DIR / f"{repo}.json"

    with open(file, "w") as f:
        json.dump(data, f)

router = APIRouter()

@router.get("/repo-graph/{repo_id}")
def repo_graph(repo_id: str):

    result = analyze_repo(repo_id)

    return result