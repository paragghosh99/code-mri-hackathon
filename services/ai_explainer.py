import json
from gemini_client import generate_text_with_retry
from prompts import SYSTEM_PROMPT
from pydantic_models import AIExplanation


DISCLAIMER = (
"Analysis is based only on visible repository files "
"and extracted dependency information."
)

def calculate_confidence(metrics):

    files_parsed = metrics.get("files_parsed", 0)
    total_files = metrics.get("total_files", 1)
    dependencies = metrics.get("dependencies", 0)

    file_coverage = files_parsed / total_files
    dependency_density = min(dependencies / 50, 1)

    stability_factor = 0.9

    confidence = (
        0.5 * file_coverage +
        0.3 * dependency_density +
        0.2 * stability_factor
    )

    return round(min(confidence, 1), 2)


def explain_scaling(metrics):

    prompt = f"""
{SYSTEM_PROMPT}

INPUT METRICS:

{json.dumps(metrics, indent=2)}

Return JSON in this format:

{{
 "confidence": float,
 "explanation": "string",
 "recommendations": ["string"]
}}
"""

    response = generate_text_with_retry(prompt)

    if response is None:
        return {
            "confidence": 0.3,
            "explanation": "AI explanation temporarily unavailable due to API rate limits.\n\nAnalysis is based only on visible repository files and extracted dependency information.",
            "recommendations": [
                "Retry analysis later when AI service quota resets",
                "Review high-centrality modules manually"
            ]
        }

    cleaned = (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    parsed = json.loads(cleaned)

    # Ensure required fields exist
    if "recommendations" not in parsed:
        parsed["recommendations"] = [
            "Further architectural analysis required."
        ]

    if "confidence" not in parsed:
        parsed["confidence"] = 0.5

    validated = AIExplanation(**parsed)

    validated.confidence = calculate_confidence(metrics)

    validated.explanation += "\n\n" + DISCLAIMER

    print("Gemini explanation:", validated.explanation)

    try:
        return validated.model_dump()
    except:
        return "AI explanation unavailable."