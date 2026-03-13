import json
from gemini_client import generate_text_with_retry

INTENT_PROMPT = """
You are an API that converts user requests into commands.

You MUST return valid JSON.

Allowed commands:

simulate_scaling
explain_risk
analyze_dependencies
show_architecture

Output format ONLY:

{
 "command": "simulate_scaling",
 "confidence": 0.95
}

DO NOT include explanation.
DO NOT include markdown.
DO NOT include text outside JSON.

User request:
"""


def detect_intent(user_query: str):

    prompt = INTENT_PROMPT + user_query

    response = generate_text_with_retry(prompt)

    try:

        cleaned = response.replace("```json", "").replace("```", "").strip()

        result = json.loads(cleaned)

        return result

    except Exception as e:

        print("Intent parse failed:", response)

        return {
            "command": "unknown",
            "confidence": 0.0
        }