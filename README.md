# 📄 AI Document Assistant

An AI-powered document assistant that enables users to upload PDF documents and ask questions using **Retrieval-Augmented Generation (RAG)**.

The system processes documents, creates semantic embeddings using **Sentence Transformers**, stores embeddings in a **FAISS** vector index, retrieves relevant document context, and uses a **Groq-powered LLM** to generate context-grounded answers.

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
- 🛡️ Context-grounded prompting to reduce hallucinations
- 🔎 Semantic similarity-based document retrieval
- 🧩 Modular document processing architecture

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
                    │     PyMuPDF      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Chunking     │
                    │  Size: 1000      │
                    │  Overlap: 200    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Embeddings    │
                    │ all-MiniLM-L6-v2 │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   FAISS Vector   │
                    │      Index       │
                    └────────┬─────────┘
                             │
                             │ User Question
                             ▼
                    ┌──────────────────┐
                    │    Retriever     │
                    │ Semantic Search  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Relevant Context │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Groq LLM     │
                    │ Answer Generation│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Final Response  │
                    └──────────────────┘
🔄 How It Works

The application follows a complete document-to-answer pipeline.

1. 📄 PDF Upload

The user uploads a PDF document through the Streamlit interface.

2. 📖 Text Extraction

The application uses PyMuPDF to extract text from the uploaded PDF.

3. ✂️ Document Chunking

The extracted text is divided into smaller overlapping chunks.

The current chunking configuration is:

Chunk Size    : 1000
Chunk Overlap : 200

Overlapping chunks help preserve contextual information between neighboring sections of the document.

4. 🧠 Embedding Generation

Each document chunk is converted into a numerical vector using the Sentence Transformer model:

all-MiniLM-L6-v2

These embeddings represent the semantic meaning of the document content.

5. 🗂️ Vector Storage

The generated embeddings are stored in a FAISS vector index.

FAISS enables efficient similarity-based search across the document embeddings.

6. 🔎 Semantic Retrieval

When the user asks a question:

User Question
      ↓
Question Embedding
      ↓
FAISS Similarity Search
      ↓
Relevant Document Chunks

The system retrieves the most relevant document content based on semantic similarity.

7. 📚 Context Construction

The retrieved document chunks are combined to create relevant context for the language model.

8. 🤖 LLM Response Generation

The retrieved context and user question are provided to a Groq-powered LLM.

The model generates an answer using the retrieved document information.

9. ✅ Final Response

The generated response is displayed to the user through the Streamlit interface.

🛠️ Tech Stack
Category	Technology
Programming Language	Python
User Interface	Streamlit
PDF Processing	PyMuPDF
Embeddings	Sentence Transformers
Embedding Model	all-MiniLM-L6-v2
Vector Search	FAISS
LLM	Groq
AI Architecture	Retrieval-Augmented Generation (RAG)
Numerical Computing	NumPy
Version Control	Git & GitHub
📁 Project Structure
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
💻 Installation
1. Clone the Repository
git clone https://github.com/Thekeshavjoshi/ai-document-assistant.git
2. Navigate to the Project Directory
cd ai-document-assistant
3. Create a Virtual Environment
python -m venv venv
4. Activate the Virtual Environment
Windows
venv\Scripts\activate
macOS / Linux
source venv/bin/activate
5. Install Dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file in the project root directory.

GROQ_API_KEY=your_groq_api_key

Replace your_groq_api_key with your actual Groq API key.

⚠️ Never commit your .env file or expose your API key publicly.

▶️ Run the Application

Start the Streamlit application using:

streamlit run app.py

The application will open in your browser.

🧪 Example Questions

After uploading a PDF document, users can ask questions such as:

What is the main topic of this document?
Summarize the key concepts discussed in the document.
What methodology is used in the research?
What are the main findings?
Explain this concept in simple terms.
What are the important points discussed in the document?
Explain the key information from this section.

The system retrieves relevant document context before generating the answer.

🔎 RAG Pipeline

The project implements a Retrieval-Augmented Generation pipeline:

                         PDF Document
                              │
                              ▼
                       Text Extraction
                              │
                              ▼
                        Text Chunking
                              │
                              ▼
                   Sentence Transformer
                              │
                              ▼
                     Vector Embeddings
                              │
                              ▼
                         FAISS Index
                              │
                              │
                       User Question
                              │
                              ▼
                     Question Embedding
                              │
                              ▼
                     Similarity Search
                              │
                              ▼
                      Relevant Chunks
                              │
                              ▼
                       Retrieved Context
                              │
                              ▼
                          Groq LLM
                              │
                              ▼
                       Grounded Answer
🧠 Technical Highlights
🔹 Semantic Search

The system uses semantic embeddings to retrieve document content based on meaning rather than relying only on exact keyword matching.

This allows the system to identify document sections that are conceptually related to the user's question.

🔹 FAISS Vector Search

FAISS is used to store document embeddings and perform similarity-based retrieval efficiently.

The retrieved vectors correspond to document chunks that are most relevant to the user's query.

🔹 Context-Grounded Generation

The retrieved document chunks are provided to the LLM as context along with the user's question.

This helps keep the generated response grounded in the uploaded document.

🔹 Overlapping Chunking

The document is divided into overlapping chunks using:

Chunk Size    : 1000
Chunk Overlap : 200

The overlap helps preserve contextual information across chunk boundaries.

🔹 Modular Architecture

The project separates different responsibilities into individual modules:

Document loading
Text extraction
Text chunking
Embedding generation
Vector storage
Semantic retrieval
RAG processing
LLM response generation

This modular structure makes the application easier to maintain and extend.

📊 Document Retrieval Flow
                     User Question
                           │
                           ▼
                   Generate Embedding
                           │
                           ▼
                 Search FAISS Index
                           │
                           ▼
               Retrieve Relevant Chunks
                           │
                           ▼
                  Build Context
                           │
                           ▼
                     Groq LLM
                           │
                           ▼
                    Final Answer

The retrieval process ensures that the LLM receives relevant information from the uploaded document instead of requiring the entire document to be passed directly into the generation step.

🎯 Use Cases

The AI Document Assistant can be used for:

📚 Research paper analysis
🎓 Academic document assistance
📑 Business document analysis
📖 Book and report analysis
🏢 Enterprise knowledge assistants
🔍 Internal document search
🤖 AI-powered knowledge bases
📄 Technical documentation analysis
📸 Demo
Application Screenshot

Add a screenshot of the working Streamlit application here.

The screenshot should ideally show:

PDF Upload
     ↓
Document Processing
     ↓
User Question
     ↓
Semantic Retrieval
     ↓
AI Generated Answer
🚧 Current Limitations
The current version primarily focuses on PDF documents.
Retrieval quality depends on document structure and chunking strategy.
Complex tables and highly visual PDF content may require additional processing.
Page-level source citations are not currently implemented.
Multi-document conversational memory is not currently implemented.
🔮 Future Improvements

Planned improvements include:

💬 Multi-turn conversational memory
📚 Multi-document support
🔎 Hybrid keyword + semantic search
📊 Retrieval relevance evaluation
🔁 Advanced document reranking
📑 Page-level source citations
⚡ Streaming LLM responses
📈 Document analytics
🗂️ Persistent vector storage
🔐 User authentication
🌐 Cloud deployment
🧠 Improved document retrieval strategies
💡 What This Project Demonstrates

This project demonstrates practical implementation of modern AI application development concepts:

Python
   ↓
Document Processing
   ↓
Text Chunking
   ↓
Embeddings
   ↓
Vector Search
   ↓
Semantic Retrieval
   ↓
RAG
   ↓
LLM
   ↓
AI Application

The project combines document processing, semantic search, vector databases, Retrieval-Augmented Generation, and Large Language Models to build a practical AI-powered document intelligence system.

📌 Project Status

🚀 Active Development

The project can be extended with improved retrieval, multi-document support, conversational memory, source citations, and cloud deployment.

👨‍💻 Author
Keshav Joshi

AI/ML Engineer | Generative AI | Agentic AI | RAG | LLMs

GitHub: https://github.com/Thekeshavjoshi
LinkedIn: https://www.linkedin.com/
⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.


### ❤️ THIS is the one, Chatsuu.

Your current README has only **3 sections**. The one above gives you the full professional structure:

**Overview → Features → Architecture → How It Works → Tech Stack → Structure → Installation → Environment → Run → Examples → RAG → Technical Highlights → Retrieval Flow → Use Cases → Demo → Limitations → Future Improvements → Project Status → Author**

Now simply:

**README → Edit ✏️ → Ctrl+A → Delete → Paste everything above → Commit changes**

Commit message:

```text
Complete AI Document Assistant README
