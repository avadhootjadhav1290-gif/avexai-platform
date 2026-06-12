# test_rag.py

from modules.rag_manager import (
    answer_with_documents
)

question = input(
    "Ask question: "
)

answer = answer_with_documents(
    question
)

print(answer)