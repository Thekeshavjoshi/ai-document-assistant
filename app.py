import streamlit as st
from pathlib import Path
import tempfile

from src.retriever import retrieve
from src.document_processor import process_document
from src.llm import (
    generate_answer,
    generate_document_summary
)


# =============================
# Page Configuration
# =============================

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="wide"
)


# =============================
# Session State Initialization
# =============================

if "document_processed" not in st.session_state:
    st.session_state["document_processed"] = False

if "document_summary" not in st.session_state:
    st.session_state["document_summary"] = None

if "vector_store_path" not in st.session_state:
    st.session_state["vector_store_path"] = None

if "document_name" not in st.session_state:
    st.session_state["document_name"] = None

if "pages" not in st.session_state:
    st.session_state["pages"] = 0

if "chunks" not in st.session_state:
    st.session_state["chunks"] = 0


# =============================
# Title
# =============================

st.title("🤖 AI Document Assistant")

st.write(
    "Upload a PDF and ask questions about "
    "its content using AI-powered RAG."
)


# =============================
# Upload PDF
# =============================

uploaded_file = st.file_uploader(
    "📄 Upload your PDF",
    type=["pdf"]
)


# =============================
# Process PDF
# =============================

if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    st.write(
        f"File size: "
        f"{uploaded_file.size / 1024:.2f} KB"
    )

    if st.button("⚙️ Process Document"):

        try:

            with st.spinner(
                "📚 Processing your document..."
            ):

                # -------------------------
                # Save uploaded PDF
                # -------------------------

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getbuffer()
                    )

                    pdf_path = Path(
                        temp_file.name
                    )

                # -------------------------
                # Create temporary vector store
                # -------------------------

                vector_store_path = (
                    Path(tempfile.mkdtemp())
                    / "vector_store"
                )

                # -------------------------
                # Process document
                # -------------------------

                result = process_document(
                    pdf_path,
                    vector_store_path
                )

                # -------------------------
                # Save session information
                # -------------------------

                st.session_state["vector_store_path"] = str(
                    vector_store_path
                )

                st.session_state["document_processed"] = True

                # Fixed typo: document_summary
                st.session_state["document_summary"] = None

                st.session_state["document_name"] = uploaded_file.name

                st.session_state["pages"] = result["pages"]

                st.session_state["chunks"] = result["chunks"]

            st.success(
                "✅ Document processed successfully!"
            )

            # -------------------------
            # Document statistics
            # -------------------------

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "📄 Pages",
                    result["pages"]
                )

            with col2:
                st.metric(
                    "🧩 Chunks",
                    result["chunks"]
                )

        except Exception as e:

            st.error(
                f"❌ Error while processing "
                f"document: {e}"
            )


# =============================
# Document Summary
# =============================

if st.session_state.get(
    "document_processed",
    False
):

    st.divider()

    st.header("📚 Document Summary")

    st.write(
        "Generate a summary of the entire uploaded PDF."
    )

    if st.button(
        "📖 Summarize Entire Document"
    ):

        try:

            with st.spinner(
                "🧠 Reading and summarizing the entire document..."
            ):

                summary = generate_document_summary(
                    st.session_state["vector_store_path"]
                )

            # Save summary in session state
            st.session_state["document_summary"] = summary

        except Exception as e:

            st.error(
                f"❌ Error while generating summary: {e}"
            )

    # -----------------------------
    # Display saved summary
    # -----------------------------

    if st.session_state.get(
        "document_summary"
    ):

        st.subheader(
            "📚 Overall Document Summary"
        )

        st.write(
            st.session_state["document_summary"]
        )


# =============================
# Ask Questions
# =============================

if st.session_state.get(
    "document_processed",
    False
):

    st.divider()

    st.header("🔍 Ask Questions")

    st.write(
        f"Ask questions about "
        f"**{st.session_state['document_name']}**"
    )

    question = st.text_input(
        "💬 Enter your question",
        placeholder=(
            "Example: What is multi-head attention?"
        )
    )

    if st.button(
        "🔎 Search Document"
    ):

        if not question.strip():

            st.warning(
                "⚠️ Please enter a question."
            )

        else:

            try:

                # =============================
                # Retrieve relevant chunks
                # =============================

                with st.spinner(
                    "🔎 Searching the document..."
                ):

                    results = retrieve(
                        question,
                        st.session_state["vector_store_path"],
                        top_k=8
                    )

                # =============================
                # Check if relevant information
                # was found
                # =============================

                if not results:

                    st.warning(
                        "⚠️ I couldn't find relevant "
                        "information in the uploaded "
                        "document."
                    )

                    st.info(
                        "Try asking a question that "
                        "is related to the document."
                    )

                else:

                    # =============================
                    # Generate Answer
                    # =============================

                    with st.spinner(
                        "🤖 Generating answer..."
                    ):

                        answer = generate_answer(
                            question,
                            results
                        )

                    # =============================
                    # Display Answer
                    # =============================

                    st.subheader(
                        "🤖 Answer"
                    )

                    st.write(answer)

                    # =============================
                    # Display Sources
                    # =============================

                    st.subheader(
                        "📚 Relevant Information"
                    )

                    for i, result in enumerate(
                        results,
                        start=1
                    ):

                        with st.expander(
                            f"📄 Result {i} — "
                            f"Page {result['page_number']}"
                        ):

                            st.write(
                                result["text"]
                            )

                            st.caption(
                                f"Cosine similarity: "
                                f"{result['similarity']:.4f}"
                            )

            except Exception as e:

                st.error(
                    f"❌ Error while searching: {e}"
                )
