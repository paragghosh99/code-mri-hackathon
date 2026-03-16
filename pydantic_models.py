from pydantic import BaseModel
from typing import List


class GenerateRequest(BaseModel):
    prompt: str


class AnalyzeRequest(BaseModel):
    image_base64: str
    instruction: str


class AnalysisResult(BaseModel):
    visible_folders: List[str]
    language_detected: str
    repo_root_structure: List[str]
    confidence: float


class PlanRequest(BaseModel):
    analysis: AnalysisResult
    files: List[str]
    visited_files: List[str]
    visited_folders: List[str]


class AIExplanation(BaseModel):
    confidence: float
    explanation: str
    recommendations: List[str]
