ANALYZE_PROMPT = """
You are an expert software architecture analyzer.

You are looking at a screenshot of a GitHub repository.

Return ONLY valid JSON.

Schema:

{
 "visible_folders": [string],
 "language_detected": string,
 "repo_root_structure": [string],
 "confidence": float
}

Rules:
- Only analyze what is visible
- Do not guess unseen files
- Do not explain
- Output ONLY JSON
"""