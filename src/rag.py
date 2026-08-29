import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from retriever import retrieve


# =================================
# Load environment variables
# =================================

load_dotenv()


# =================================
# Groq client
# =================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =================================
# Generate Answer
# =================================

def generate_answer(
    question,
    vector_store_path,
    top_k=8
):

    # ---------------------------------
    # Retrieve relevant chunks
    # ---------------------------------

    results = retrieve(
        query=question,
        vector_store_path=vector_store_path,
        top_k=top_k
    )

    # ---------------------------------
    # Handle no relevant information
    # ---------------------------------

    if not results:

        return (
            "I could not find the answer in "
            "the provided document.",
            []
        )

    # ---------------------------------
    # Build document context
    # ---------------------------------

    context_parts = []

    for i, result in enumerate(
        results,
        start=1
    ):

        context_parts.append(
            f"""
[Context {i}]
Page: {result['page_number']}
Similarity: {result['similarity']:.4f}

{result['text']}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    # ---------------------------------
    # Prompt
    # ---------------------------------

    prompt = f"""
You are an AI document research assistant.

Your task is to answer the user's question
using ONLY the information contained in the
provided document context.

IMPORTANT RULES:

1. Do NOT use outside knowledge.
2. Do NOT invent or assume information.
3. Prefer information from contexts with
   higher similarity scores.
4. Ignore context that is not relevant to
   the user's question.
5. If the answer requires information from
   multiple contexts, combine them carefully.
6. Give a clear and concise answer.
7. When useful, mention the page number
   where the information was found.
8. If the answer cannot be found in the
   provided context, say exactly:

"I could not find the answer in the
provided document."

DOCUMENT CONTEXT
================

{context}

================

USER QUESTION
=============

{question}

=============

Now answer the question using only the
document context.
"""

    # ---------------------------------
    # Generate answer using Groq
    # ---------------------------------

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document-grounded "
                    "AI research assistant. "
                    "Never use outside knowledge "
                    "when answering questions."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )

    # ---------------------------------
    # Extract answer
    # ---------------------------------

    answer = (
        response
        .choices[0]
        .message
        .content
    )

    # ---------------------------------
    # Source pages
    # ---------------------------------

    sources = sorted(
        set(
            result["page_number"]
            for result in results
        )
    )

    return answer, sources


# =================================
# Local testing
# =================================

if __name__ == "__main__":

    project_root = (
        Path(__file__).resolve().parent.parent
    )

    vector_store_path = (
        project_root
        / "data"
        / "test_vector_store"
    )

    question = (
        "What is multi-head attention?"
    )

    answer, sources = generate_answer(
        question=question,
        vector_store_path=vector_store_path,
        top_k=8
    )

    print(
        "\n=============================="
    )

    print(
        "Question:"
    )

    print(question)

    print(
        "\nAnswer:"
    )

    print(answer)

    print(
        "\nSources:"
    )

    for page in sources:

        print(
            f"- Attention Is All You Need "
            f"— Page {page}"
        )