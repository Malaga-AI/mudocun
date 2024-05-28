import os
from time import time
from urllib.parse import urlparse

import requests
import vertexai
import vertexai.preview.generative_models as generative_models
from dotenv import load_dotenv
from vertexai.generative_models import FinishReason, GenerativeModel, Part

from prompts import zero_shot_prompt

# Define variables
load_dotenv()
REGION = os.getenv("REGION")
PROJECT = os.getenv("PROJECT")
MODEL = "gemini-1.5-pro-001"
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0.0, # Make results reproducible
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


def read_document_file(pdf_document_path):
    with open(pdf_document_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
        return Part.from_data(mime_type="application/pdf", data=pdf_bytes)


def fetch_document(pdf_document_url):
    response = requests.get(pdf_document_url)
    response.raise_for_status()
    return Part.from_data(mime_type="application/pdf", data=response.content)


# Utility functions
def generate_quiz(document, reference_document=None):
    print(f"Generating quiz for document \"{document["title"]}\"...")
    uri = document["uri"]
    pdf_document = fetch_document(uri) if not is_local(uri) else read_document_file(uri)
    start = time()
    response = model.generate_content(
        [zero_shot_prompt, pdf_document],
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    request_time = time() - start
    return (
        response.text,
        response.usage_metadata.prompt_token_count,     # input tokens
        response.usage_metadata.candidates_token_count, # output tokens
        request_time
    )
