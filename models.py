from pydantic import BaseModel, Field
from typing_extensions import TypedDict


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


# class MultipleChoiceQuestion(TypedDict):
#     """Multiple choice question over a figure or formula in a scientific publication.

#     Attributes:
#         text: The text of the question.
#         choices: A list of choices for the question.
#             The list should contain 4 choices (A-D multiple choice).
#         correct_answer_idx: The index of the correct answer from the list of choices.
#     """

#     text: str
#     choices: list[str]
#     correct_answer_idx: int


class QuestionMetadata(TypedDict):
    is_valid: bool
    is_validated_by_model: bool
    is_validated_by_human: bool
    explanation: str | None


class QuizQuestion(TypedDict):
    multiple_choice_question: MultipleChoiceQuestion
    metadata: QuestionMetadata


class QuizMetadata(TypedDict):
    model: str
    region: str
    num_input_tokens: int
    num_output_tokens: int
    generation_time: float
    timestamp: float


class Article(TypedDict):
    title: str
    uri: str

    def __init__(self, dict):
        self.title = dict["title"]
        self.uri = dict["uri"]


class Quiz(TypedDict):
    article: Article
    questions: list[QuizQuestion]
    metadata: QuizMetadata
