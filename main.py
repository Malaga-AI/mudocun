import argparse
import logging
import os
import sys
import time
from datetime import timedelta

import pandas as pd
import requests

from docs import online_documents
from models import (
    Article,
    FailedGeneration,
    FailedQuiz,
    QuestionMetadata,
    Quiz,
    QuizMetadata,
    QuizQuestion,
)
from vertexai_utils import generate_questions, generate_structured_questions

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)


def get_pending_articles(
    documents: list[Article],
    output_dir: str,
    refresh: bool,
) -> list[tuple[int, Article]]:
    pending_articles = []
    if refresh:
        for idx, document in enumerate(documents):
            pending_articles.append((idx, document))
    else:
        filenames = [
            f.split(".")[0]
            for f in os.listdir(output_dir)
            if os.path.isfile(os.path.join(output_dir, f))
        ]
        for idx, document in enumerate(documents):
            if document.filename(idx) not in filenames:
                pending_articles.append((idx, document))

    return pending_articles


def get_arxiv_docs(max_num_articles: int | None = None) -> list[Article]:
    response = requests.get(
        "https://raw.githubusercontent.com/paperscape/paperscape-data/master/pscp-2017.csv"
    )
    response.raise_for_status()
    csv = response.text.split("\n")

    entries = [line.split(";", 7) for line in csv if not line.startswith("#")]
    df = pd.DataFrame(entries)
    df_sorted = df.sort_values(by=3, ascending=False)[[0, 6]]
    if max_num_articles:
        df_sorted = df_sorted[:max_num_articles]

    selected_articles = df_sorted.apply(
        lambda row: Article(title=str(row[6]), uri=f"https://arxiv.org/pdf/{row[0]}"),
        axis=1,
    )

    return selected_articles.tolist()


def generate_quiz(article: Article) -> Quiz:
    # 1. Generate questions
    questions, creation_metadata = generate_questions(article)

    # 2. Structure the questions
    structured_questions, structuring_metadata = generate_structured_questions(
        questions
    )

    # 3. Create quiz object
    metadata = QuizMetadata(
        creation_metadata=creation_metadata,
        structuring_metadata=structuring_metadata,
    )
    quiz_questions = [
        QuizQuestion(
            multiple_choice_question=q, metadata=QuestionMetadata(is_validated=False)
        )
        for q in structured_questions
    ]
    return Quiz(
        article=article,
        questions=quiz_questions,
        metadata=metadata,
    )


def main(refresh: bool, arxiv_docs: bool, output_dir: str, failed_dir: str):
    documents = (
        get_arxiv_docs() if arxiv_docs else [Article(**d) for d in online_documents]
    )
    pending_articles = get_pending_articles(documents, refresh, output_dir)
    start_time = time.time()
    num_failed_articles = 0

    for idx, article in pending_articles:
        logging.debug(f"Processing article {idx}: {article.title}")
        filename = article.filename(idx)
        try:
            quiz = generate_quiz(article)
            file_path = os.path.join(output_dir, filename + ".json")
            with open(file_path, "w") as output_file:
                output_file.write(quiz.model_dump_json())
            logging.info(
                f"SUCCESS: Quiz for article {idx}: {article.title} stored at {file_path}"
            )
        except FailedGeneration as e:
            num_failed_articles += 1
            failed_quiz = FailedQuiz(
                article=article, reason=str(e), metadata=e.metadata, response=e.response
            )
            file_path = os.path.join(
                failed_dir, filename + "_" + e.metadata.timestamp + ".json"
            )
            logging.warning(
                f"FAILED: Quiz for article {idx}: {article.title} failed. Storing info at {file_path}"
            )
            with open(file_path, "w") as output_file:
                output_file.write(failed_quiz.model_dump_json())

        time.sleep(0.5)  # Quick and dirty way to prevent rate-limiting

    stop_time = time.time()
    total_time = timedelta(seconds=stop_time - start_time)
    logging.info(
        f"Processed {len(pending_articles)} articles in {str(total_time).split('.')[0]} ({num_failed_articles} failed)"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--arxiv-docs", action="store_true")
    parser.add_argument("--output-dir", type=str, default="./outputs")
    parser.add_argument("--failed-dir", type=str, default="./outputs/failed")
    args = parser.parse_args()

    main(args.refresh, args.arxiv_docs, args.output_dir, args.failed_dir)
