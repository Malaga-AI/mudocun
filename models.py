import re
from enum import Enum, auto
from typing import Any

from pydantic import BaseModel, Field


class Article(BaseModel):
    title: str
    uri: str

    def filename(self, index: int) -> str:
        return f"{str(index).zfill(4)}-{re.sub(r'[\/\\]+|\s+', '_', self.title)}"


class MultipleChoiceQuestion(BaseModel):
    """Multiple choice question over a figure or formula in a scientific publication."""

    text: str = Field(..., description="The text of the question")
    choices: list[str] = Field(
        ...,
        description="A list of choices for the question. The list should contain 4 choices (A-D multiple choice).",
    )
    correct_answer_idx: int = Field(
        ..., description="The index of the correct answer from the list of choices."
    )


class QuestionMetadata(BaseModel):
    is_validated: bool
    validator: str | None = None
    explanation: str | None = None


class QuizQuestion(BaseModel):
    multiple_choice_question: MultipleChoiceQuestion
    metadata: QuestionMetadata


class GenerationMetadata(BaseModel):
    model: str
    region: str | None = None
    num_input_tokens: int | None = None
    num_output_tokens: int | None = None
    generation_time: float
    timestamp: str


class GenerationStage(Enum):
    CREATION = auto()
    STRUCTURING = auto()
    PARSING = auto()


class FailedGeneration(Exception):
    stage: GenerationStage
    metadata: GenerationMetadata
    response: str | None

    def __init__(
        self,
        message: Any,
        stage: GenerationStage,
        metadata: GenerationMetadata,
        response: str | None = None,
    ):
        super().__init__(message)
        self.stage = stage
        self.metadata = metadata
        self.response = response


class FailedQuiz(BaseModel):
    article: Article
    reason: str
    metadata: GenerationMetadata
    response: str | None


class QuizMetadata(BaseModel):
    creation_metadata: GenerationMetadata | None
    structuring_metadata: GenerationMetadata | None


class Quiz(BaseModel):
    article: Article
    questions: list[QuizQuestion]
    metadata: QuizMetadata
