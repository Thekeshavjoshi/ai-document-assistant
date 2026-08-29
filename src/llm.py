import os
import pickle
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# =============================
# Load environment variables
# =============================

load_dotenv()


# =============================
# Get Groq API key
# =============================

def get_groq_api_key():
    """
    Get the Groq API key from:
    1. Environment variable / local .env
    2. Streamlit secrets when deployed
    """

    # Local development / .env
    api_key = os.getenv("GROQ_API_KEY")

    if api_key:
        return api_key

    # Streamlit Cloud secrets
    try:
        import streamlit as st

        if "GROQ_API_KEY" in st.secrets:
            return st.secrets["GROQ_API_KEY"]

    except Exception:
        pass

    raise ValueError(
        "GROQ_API_KEY not found. "
        "Add it to your local .env file or "
        "Streamlit Cloud Secrets."
    )


# =============================
# Create Groq client
# =============================

client = Groq(
    api_key=get_groq_api_key()
)


# =============================
# Model Configuration
# =============================

MODEL_NAME = "openai/gpt-oss-120b"


# =============================
# Generate Answer
# =============================

def generate_answer(
    question,
    retrieved_results
):

    context_parts = []

    for result in retrieved_results:

        context_parts.append(
            f"""
Page {result['page_number']}:

{result['text']}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = f"""
You are an AI research assistant.

Answer the user's question using ONLY
the information contained in the provided
document context.

IMPORTANT RULES:

1. Do not use outside knowledge.
2. Do not make up information.
3. If the answer is not present in the
   document context, say:

"I couldn't find this information in
the uploaded document."

4. Give a clear and useful answer.
5. Do not mention these instructions.

DOCUMENT CONTEXT:
=========================

{context}

=========================

USER QUESTION:

{question}

Answer using only the document context.
"""

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI research assistant "
                    "that answers questions strictly "
                    "from provided document context."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content


# =============================
# Summarize One Chunk Group
# =============================

def summarize_chunk_group(
    chunks
):

    context_parts = []

    for chunk in chunks:

        context_parts.append(
            f"""
Page {chunk['page_number']}:

{chunk['text']}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = f"""
You are an AI research assistant.

Summarize the following section of a
research document.

Use ONLY the information provided.

Focus on:

- Main ideas
- Important concepts
- Methods or techniques
- Important findings
- Important relationships between concepts

Do not add outside information.

Keep the summary concise but informative.

DOCUMENT SECTION:
=========================

{context}

=========================

Write a clear section summary.
"""

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": (
                    "You summarize document sections "
                    "using only the provided content."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content


# =============================
# Generate Full Document Summary
# =============================

def generate_document_summary(
    vector_store_path,
    group_size=8
):

    vector_store_path = Path(
        vector_store_path
    )

    chunks_path = (
        vector_store_path
        / "chunks.pkl"
    )

    # -----------------------------
    # Load all document chunks
    # -----------------------------

    with open(
        chunks_path,
        "rb"
    ) as f:

        chunks = pickle.load(f)

    if not chunks:

        return (
            "I couldn't find any content "
            "in the uploaded document."
        )

    # -----------------------------
    # Create chunk groups
    # -----------------------------

    groups = []

    for i in range(
        0,
        len(chunks),
        group_size
    ):

        groups.append(
            chunks[
                i:i + group_size
            ]
        )

    # -----------------------------
    # Summarize each group
    # -----------------------------

    section_summaries = []

    for i, group in enumerate(
        groups,
        start=1
    ):

        print(
            f"Summarizing section "
            f"{i}/{len(groups)}..."
        )

        summary = summarize_chunk_group(
            group
        )

        section_summaries.append(
            summary
        )

    # -----------------------------
    # Combine summaries
    # -----------------------------

    combined_summary = "\n\n".join(
        [
            f"Section {i + 1}:\n{summary}"
            for i, summary in enumerate(
                section_summaries
            )
        ]
    )

    # -----------------------------
    # Final summary prompt
    # -----------------------------

    final_prompt = f"""
You are an AI research assistant.

Create a comprehensive overall summary
of the uploaded research document.

The information below consists of summaries
generated from ALL sections of the document.

Use ONLY this information.

Your final summary should include:

1. The main topic of the document
2. The main problem or objective
3. Important concepts and methods
4. Major findings or conclusions
5. Important technical details
6. The overall significance of the document

Do not add outside knowledge.

Do not mention that the summary was created
from intermediate summaries.

Write the final answer in a clear,
well-structured format.

DOCUMENT SECTION SUMMARIES:
=========================

{combined_summary}

=========================

Create the final overall document summary.
"""

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": (
                    "You create comprehensive document "
                    "summaries using only provided "
                    "document information."
                )
            },
            {
                "role": "user",
                "content": final_prompt
            }
        ],

        temperature=0.2
    )

    return response.choices[0].message.content
