import os
from time import time
from urllib.parse import urlparse

import requests
import vertexai
import vertexai.generative_models
from dotenv import load_dotenv
from vertexai.generative_models import (FunctionDeclaration, GenerativeModel,
                                        Part, Tool)
from vertexai.preview.generative_models import (HarmBlockThreshold,
                                                HarmCategory, ToolConfig)

from models import (Article, MultipleChoiceQuestion, Quiz, QuizMetadata,
                    QuizQuestion)
from prompts import create_quiz_prompt

# Define variables
load_dotenv()
REGION = os.getenv("REGION")
PROJECT = os.getenv("PROJECT")
MODEL = "gemini-1.5-pro-001"
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1.0,
    "top_p": 0.95,
}
safety_settings = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}


# Helper functions
def is_local(uri: str) -> bool:
    return urlparse(uri).scheme in ["file", ""]


def read_document_file(pdf_document_path: str) -> Part:
    with open(pdf_document_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
        return Part.from_data(mime_type="application/pdf", data=pdf_bytes)


def fetch_document(pdf_document_url) -> Part:
    response = requests.get(pdf_document_url)
    response.raise_for_status()
    return Part.from_data(mime_type="application/pdf", data=response.content)


# Function calling
def create_quiz(questions: list[MultipleChoiceQuestion]):
    """"Create a quiz from the given multiple choice questions.

    Args:
        questions: list of multiple choice questions for the quiz.
    """
    return questions

# Model startup
vertexai.init(project=PROJECT, location=REGION)
model = GenerativeModel(MODEL)
#model_with_tools = GenerativeModel(MODEL, tools=[create_quiz])

# Utility functions
def generate_quiz(document: Article):
    print(f"Generating quiz for document \"{document["title"]}\"...")
    uri = document["uri"]
    pdf_document = fetch_document(uri) if not is_local(uri) else read_document_file(uri)
    start = time()
    response = model.generate_content(
        [create_quiz_prompt, pdf_document],
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

create_quiz_func = FunctionDeclaration(
    name=create_quiz.__name__,
    description=create_quiz.__doc__,
    #parameters=MultipleChoiceQuestion.model_json_schema()  # Does not pick as a list
    parameters = {
        "type": "array",
        "properties": {
            "questions": {
                "type": "array",
                "description": "list of multiple choice questions for the quiz",
                "items": MultipleChoiceQuestion.model_json_schema()
            },
        },
        "required": [
            "questions"
        ]
    }
)


tools = [
    Tool(function_declarations=[create_quiz_func])
]

# Doesn't work with the following error, despite using a Gemini 1.5 pro model:
# 400 Unable to submit request because the forced function calling (mode = ANY) is only supported for Gemini 1.5 Pro models.
# Learn more: https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling

# tool_config = ToolConfig(
#     function_calling_config=ToolConfig.FunctionCallingConfig(
#         mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
#         allowed_function_names=[create_quiz.__name__],
#     )
# )

# Can't generate structured output directly due to error:
# InvalidArgument: 400 Unable to submit request because Function Calling is not supported with non-text input.
# Remove the function declarations or remove inline_data/file_data from contents.
# Learn more: https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling

def generate_structured_quiz(questions: str):
    print(f"Generating structured quiz...")
    start = time()
    response = model.generate_content(
        questions.format(questions=questions),
        generation_config=generation_config,
        safety_settings=safety_settings,
        tools=tools,
        #tool_config=tool_config # Doesn't work
    )
    request_time = time() - start
    return response
