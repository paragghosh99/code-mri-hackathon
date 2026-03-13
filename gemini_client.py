from dotenv import load_dotenv
import base64
import os
from google import genai
import vertexai
from vertexai.generative_models import GenerativeModel
from google.genai.types import Part
from vertexai.generative_models import Part as vPart
import json
import time

REQUEST_TIMEOUT = 20

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODE = os.getenv("GEMINI_MODE", "studio")

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION", "us-central1")


# ---------- AI STUDIO CLIENT ----------

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

    start = time.time()

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    if time.time() - start > REQUEST_TIMEOUT:
        raise TimeoutError("Gemini request timed out")

    return response.text


model = GenerativeModel("gemini-2.5-flash")

vertexai.init(project=PROJECT_ID, location=REGION)

# ---------- VERTEX CLIENT ----------
def vertex_generate_multimodal(prompt: str, image_base64: str):

    image_bytes = base64.b64decode(image_base64)

    response = model.generate_content([
        prompt,
        vPart.from_data(
            mime_type="image/jpeg",
            data=image_bytes
        )
    ])

    cleaned = response.text.replace("```json", "").replace("```", "").strip()

    return json.loads(cleaned)


# ---------- VERTEX TEXT ----------
def vertex_generate_text(prompt: str):

    start = time.time()

    vertexai.init(project=PROJECT_ID, location=REGION)

    model = GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    if time.time() - start > REQUEST_TIMEOUT:
        raise TimeoutError("Gemini request timed out")

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

MAX_RETRIES = 3


def generate_text_with_retry(prompt: str):

    for attempt in range(MAX_RETRIES):

        try:

            result = generate_text(prompt)

            return result

        except Exception as e:

            print(f"Gemini attempt {attempt+1} failed:", e)

            if attempt == MAX_RETRIES - 1:
                return None

            time.sleep(2)