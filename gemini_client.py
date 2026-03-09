from dotenv import load_dotenv
load_dotenv()

import os
from google import genai
import vertexai
from vertexai.generative_models import GenerativeModel

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODE = os.getenv("GEMINI_MODE", "studio")

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION", "us-central1")

# ---------- AI STUDIO CLIENT ----------
# studio_client = genai.Client(api_key=API_KEY)


def studio_generate(prompt: str):

    studio_client = genai.Client(api_key=API_KEY)

    response = studio_client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# ---------- VERTEX CLIENT ----------
def vertex_generate(prompt: str):

    vertexai.init(project=PROJECT_ID, location=REGION)

    model = GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    return response.text


# ---------- ROUTER ----------
def generate_text(prompt: str):

    if GEMINI_MODE == "vertex":
        return vertex_generate(prompt)
    
    return studio_generate(prompt)