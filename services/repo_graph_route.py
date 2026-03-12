from fastapi import APIRouter
from services.dependency_graph import analyze_repo

router = APIRouter()

@router.get("/repo-graph/{repo_id}")
def repo_graph(repo_id: str):

    result = analyze_repo(repo_id)

    return result