import os
from datetime import UTC, datetime
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
vertexai.init(project=PROJECT, location=REGION)
model = GenerativeModel(MODEL)


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

def create_quiz(questions: list[MultipleChoiceQuestion]):
    """"Create a quiz from the given multiple choice questions.

    Args:
        questions: list of multiple choice questions for the quiz.
    """
    return questions

create_quiz_func = FunctionDeclaration(
    name=create_quiz.__name__,
    description=create_quiz.__doc__,
    parameters = {
        "type": "object",
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

# Using ToolConfig doesn't work with the following error, despite using a Gemini 1.5 pro model:
# 400 Unable to submit request because the forced function calling (mode = ANY) is only supported for Gemini 1.5 Pro models.
# Learn more: https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling

# tool_config = ToolConfig(
#     function_calling_config=ToolConfig.FunctionCallingConfig(
#         mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
#         allowed_function_names=[create_quiz.__name__],
#     )
# )

# We can't generate structured output directly due to error:
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
    generation_time = time() - start

    func = response.candidates[0].content.parts[0].function_call
    func_dict = type(func).to_dict(func)    # Convert from Google Protocol Buffer to dict

    print(f"func_dict={func_dict}")

    questions = create_quiz(**func_dict["args"])

    metadata = QuizMetadata(
        model=model._model_name,
        region=REGION,
        num_input_tokens=response.usage_metadata.prompt_token_count,
        num_output_tokens=response.usage_metadata.candidates_token_count,
        generation_time=generation_time,
        timestamp=str(datetime.now(UTC))
    )

    return questions, metadata
