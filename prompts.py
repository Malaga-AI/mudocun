create_quiz_prompt = "For each figure or formula in this scientific article, create a A-D multiple choice quiz, including correct answer"
structure_quiz_prompt = """Given the following multiple choice questions for a scientific article:
----
{questions}
----

Create a quiz object with function `create_quiz`.
"""
