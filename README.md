# 📄 AI Document Assistant

An AI-powered document assistant that allows users to upload PDF documents and ask questions using Retrieval-Augmented Generation (RAG).

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
---

## 🔄 How It Works

### 1. Document Upload
The user uploads a PDF through the Streamlit interface.

### 2. Text Extraction
The system extracts text from the PDF using PyMuPDF.

### 3. Document Chunking
The extracted text is divided into smaller overlapping chunks to improve retrieval quality.

### 4. Embedding Generation
Each document chunk is converted into a vector representation using the `all-MiniLM-L6-v2` Sentence Transformer model.

### 5. Vector Storage
The generated embeddings are normalized and stored in a FAISS vector index for efficient similarity search.

### 6. Query Retrieval
When the user asks a question, the query is converted into an embedding and compared against the document vectors to retrieve relevant chunks.

### 7. LLM Generation
The retrieved context is provided to a Groq-powered LLM, which generates an answer based on the information available in the document.

### 8. Final Response
The generated response is displayed to the user through the Streamlit interface.

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python |
| User Interface | Streamlit |
| PDF Processing | PyMuPDF |
| Embeddings | Sentence Transformers |
| Embedding Model | `all-MiniLM-L6-v2` |
| Vector Search | FAISS |
| LLM | Groq |
| AI Architecture | Retrieval-Augmented Generation (RAG) |
| Numerical Processing | NumPy |
| Version Control | Git & GitHub |

---

## 📁 Project Structure

```text
ai-document-assistant/
│
├── data/
│   └── papers/
│
├── src/
│   ├── chunking.py
│   ├── document_loader.py
│   ├── document_processor.py
│   ├── embedding.py
│   ├── llm.py
│   ├── rag.py
│   ├── retriever.py
│   └── vector_store.py
│
├── app.py
├── test_processor.py
├── requirements.txt
├── .gitignore
└── README.md
