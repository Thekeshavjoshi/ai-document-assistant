from pathlib import Path

from sentence_transformers import SentenceTransformer

from chunking import create_chunks
from document_loader import load_pdf


# Project root
project_root = Path(__file__).resolve().parent.parent


if __name__ == "__main__":

    # PDF path
    pdf_path = (
        project_root
        / "data"
        / "papers"
        / "attention_is_all_you_need.pdf"
    )

    # Load PDF
    text = load_pdf(pdf_path)

    # Create chunks
    chunks = create_chunks(text)

    print(f"\nTotal chunks: {len(chunks)}")

    # Load embedding model
    print("\nLoading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Embedding model loaded!")

    # Generate embeddings
    embeddings = model.encode(chunks)

    print(f"\nEmbeddings created successfully!")
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding dimension: {embeddings.shape[1]}")