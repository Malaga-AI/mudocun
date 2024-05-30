import logging
import os
from datetime import UTC, datetime
from time import time
from urllib.parse import urlparse

import requests
import vertexai
import vertexai.generative_models
from dotenv import load_dotenv
from vertexai.generative_models import FunctionDeclaration, GenerativeModel, Part, Tool
from vertexai.preview.generative_models import (
    HarmBlockThreshold,
    HarmCategory,
    ToolConfig,
)

from models import (
    Article,
    FailedGeneration,
    FailedQuiz,
    GenerationMetadata,
    GenerationStage,
    MultipleChoiceQuestion,
    Quiz,
    QuizMetadata,
)
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


def generate_questions(article: Article) -> tuple[str, GenerationMetadata]:
    logging.debug(f'Generating quiz for document "{article.title}"...')
    uri = article.uri

    try:
        pdf_document = (
            fetch_document(uri) if not is_local(uri) else read_document_file(uri)
        )
        start = time()
        response = model.generate_content(
            [create_quiz_prompt, pdf_document],
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        generation_time = time() - start
    except Exception as e:
        raise FailedGeneration(
            message=e,
            stage=GenerationStage.CREATION,
            metadata=GenerationMetadata(
                model=model._model_name,
                region=REGION,
                generation_time=0.0,
                timestamp=str(datetime.now(UTC)),
            ),
        )

    metadata = GenerationMetadata(
        model=model._model_name,
        region=REGION,
        num_input_tokens=response.usage_metadata.prompt_token_count,
        num_output_tokens=response.usage_metadata.candidates_token_count,
        generation_time=generation_time,
        timestamp=str(datetime.now(UTC)),
    )
    return (response.text, metadata)


def create_quiz(questions: list[MultipleChoiceQuestion]):
    """ "Create a quiz from the given multiple choice questions.

    Args:
        questions: list of multiple choice questions for the quiz.
    """
    return questions


create_quiz_func = FunctionDeclaration(
    name=create_quiz.__name__,
    description=create_quiz.__doc__,
    parameters={
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "description": "list of multiple choice questions for the quiz",
                "items": MultipleChoiceQuestion.model_json_schema(),
            },
        },
        "required": ["questions"],
    },
)
tools = [Tool(function_declarations=[create_quiz_func])]

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


def generate_structured_questions(
    structured_questions: str,
) -> tuple[list[MultipleChoiceQuestion], GenerationMetadata]:
    logging.debug(f"Generating structured quiz...")
    start = time()

    try:
        response = model.generate_content(
            structured_questions.format(questions=structured_questions),
            generation_config=generation_config,
            safety_settings=safety_settings,
            tools=tools,
            # tool_config=tool_config # Doesn't work
        )
    except Exception as e:
        raise FailedGeneration(
            message=e,
            stage=GenerationStage.STRUCTURING,
            metadata=GenerationMetadata(
                model=model._model_name,
                region=REGION,
                generation_time=time() - start,
                timestamp=str(datetime.now(UTC)),
            ),
            response=structured_questions,
        )

    generation_time = time() - start

    metadata = GenerationMetadata(
        model=model._model_name,
        region=REGION,
        num_input_tokens=response.usage_metadata.prompt_token_count,
        num_output_tokens=response.usage_metadata.candidates_token_count,
        generation_time=generation_time,
        timestamp=str(datetime.now(UTC)),
    )

    try:
        func = response.candidates[0].content.parts[0].function_call
        func_dict = type(func).to_dict(
            func
        )  # Convert from Google Protocol Buffer to dict
        structured_questions = create_quiz(**func_dict["args"])
    except Exception as e:
        raise FailedGeneration(
            message=e,
            stage=GenerationStage.PARSING,
            metadata=metadata,
            response=response,
        )

    return structured_questions, metadata
