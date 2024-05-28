import os
from urllib.parse import urlparse

import vertexai
import vertexai.preview.generative_models as generative_models
from dotenv import load_dotenv
from vertexai.generative_models import FinishReason, GenerativeModel, Part

from prompts import few_shot_prompt, zero_shot_prompt

# Define variables
load_dotenv()
REGION = os.getenv("REGION")
PROJECT = os.getenv("PROJECT")
MODEL = "gemini-1.5-pro-001"
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.5,
    "top_p": 0.95,
}
safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# Model startup
vertexai.init(project=PROJECT, location=REGION)
model = GenerativeModel(MODEL)


# Helper functions
def is_local(uri):
    return urlparse(uri).scheme in ["file", ""]

def get_pdf_data(pdf_document_uri):
    if is_local(pdf_document_uri):
        with open(pdf_document_uri, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            return Part.from_data(mime_type="application/pdf", data=pdf_bytes)
    return Part.from_uri(pdf_document_uri, mime_type="application/pdf")


# Utility functions
def generate_quiz(document, reference_document=None):
    print(f"Generating quiz for document \"{document["title"]}\"...")
    pdf_document = get_pdf_data(document["uri"])
    response = model.generate_content(
        [zero_shot_prompt, pdf_document],
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    return response.text
