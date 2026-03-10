from dotenv import load_dotenv
load_dotenv()

import base64
import os
from google import genai
import vertexai
from vertexai.generative_models import GenerativeModel
from google.genai.types import Part
import json

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODE = os.getenv("GEMINI_MODE", "studio")

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION", "us-central1")

# ---------- AI STUDIO CLIENT ----------
# studio_client = genai.Client(api_key=API_KEY)

def studio_generate_multimodal(prompt: str, image_base64: str):

    client = genai.Client(api_key=API_KEY)

    image_bytes = base64.b64decode(image_base64)

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=[
            prompt,
            Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg"
            )
        ]
    )

    cleaned = response.text.replace("```json", "").replace("```", "").strip()

    return json.loads(cleaned)
# ---------- AI STUDIO TEXT ----------
def studio_generate_text(prompt: str):

    client = genai.Client(api_key=API_KEY)

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# ---------- VERTEX CLIENT ----------
def vertex_generate_multimodal(prompt: str, image_base64: str):    

    vertexai.init(project=PROJECT_ID, location=REGION)

    image_bytes = base64.b64decode(image_base64)

    model = GenerativeModel("gemini-2.5-flash")

    response = model.generate_content([
        {
            "type": "text",
            "text": prompt
        },
        {
            "type": "image",
            "mime_type": "image/jpeg",
            "data": image_bytes
        }
    ])

    return response.text


# ---------- VERTEX TEXT ----------
def vertex_generate_text(prompt: str):

    vertexai.init(project=PROJECT_ID, location=REGION)

    model = GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    return response.text


# ---------- ROUTER ----------
def generate_multimodal(prompt: str, image_base64: str):

    if GEMINI_MODE == "vertex":
        return vertex_generate_multimodal(prompt, image_base64)

    return studio_generate_multimodal(prompt, image_base64)


# ---------- TEXT ROUTER ----------
def generate_text(prompt: str):

    if GEMINI_MODE == "vertex":
        return vertex_generate_text(prompt)

    return studio_generate_text(prompt)