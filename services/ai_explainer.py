import json
from gemini_client import generate_text
from prompts import SYSTEM_PROMPT


def explain_scaling(metrics):

    prompt = f"""
{SYSTEM_PROMPT}

INPUT METRICS:

{json.dumps(metrics, indent=2)}

Explain the architectural scaling risks.
Return ONLY the explanation text.
"""

    response_text = generate_text(prompt)

    cleaned = response_text.replace("```", "").strip()

    print("Gemini explanation:", cleaned)

    try:
        return cleaned
    except:
        return "AI explanation unavailable."