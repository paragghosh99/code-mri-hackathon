from pydantic import BaseModel
from typing import List

class GenerateRequest(BaseModel):
    prompt: str

class AnalyzeRequest(BaseModel):
    instruction: str
    image_base64: str

class AnalysisResult(BaseModel):
    visible_folders: List[str]
    language_detected: str
    repo_root_structure: List[str]
    confidence: float


class PlanRequest(BaseModel):
    analysis: AnalysisResult