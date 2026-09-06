# 📄 AI Document Assistant

An AI-powered document assistant that allows users to upload PDF documents and ask questions using **Retrieval-Augmented Generation (RAG)**.

The system processes documents, creates semantic embeddings, stores them in a FAISS vector index, retrieves relevant document context, and uses a Groq-powered LLM to generate grounded answers.

---

## 🚀 Key Features

- 📄 Upload and process PDF documents
- 🔍 Semantic document search using FAISS
- 🧠 Sentence Transformer embeddings
- 📚 Retrieval-Augmented Generation (RAG)
- 🤖 Groq-powered LLM response generation
- ✂️ Intelligent document chunking with overlap
- 🎯 Context-based question answering
- 🖥️ Interactive Streamlit interface
- 🛡️ Prompting designed to reduce hallucinations by restricting answers to retrieved document context

---

## 🧠 System Architecture

```text
              ┌──────────────────┐
              │    PDF Upload    │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Text Extraction  │
              │    PyMuPDF       │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │    Chunking      │
              │  Size: 1000      │
              │ Overlap: 200     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │    Embeddings    │
              │ Sentence         │
              │ Transformers     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │  FAISS Vector    │
              │      Store       │
              └────────┬─────────┘
                       │
                       │ User Question
                       ▼
              ┌──────────────────┐
              │ Semantic         │
              │ Retrieval        │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Relevant Context │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │    Groq LLM      │
              │ Answer Generation│
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Final Response   │
              └──────────────────┘
