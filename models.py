from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class Article(TypedDict):
    title: str
    uri: str


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


class QuestionMetadata(TypedDict):
    is_validated: bool
    validator: str | None = None
    explanation: str | None = None


class QuizQuestion(TypedDict):
    multiple_choice_question: MultipleChoiceQuestion
    metadata: QuestionMetadata

    def __init__(self, multiple_choice_question: MultipleChoiceQuestion):
        self.multiple_choice_question = multiple_choice_question
        self.metadata = QuestionMetadata(is_validated=False)


class QuizMetadata(TypedDict):
    model: str
    region: str | None
    num_input_tokens: int
    num_output_tokens: int
    generation_time: float
    timestamp: str


class Quiz(TypedDict):
    article: Article
    questions: list[QuizQuestion]
    metadata: QuizMetadata

    def __init__(
        self,
        article: Article,
        multiple_choice_questions: list[MultipleChoiceQuestion],
        quiz_metadata: QuizMetadata,
    ):
        self.article = article
        self.questions = [QuizQuestion(q) for q in multiple_choice_questions]
        self.metadata = quiz_metadata
