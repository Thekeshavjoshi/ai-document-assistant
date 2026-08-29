from pathlib import Path
import pickle

import faiss
from sentence_transformers import SentenceTransformer

from src.document_loader import load_pdf
from src.chunking import create_chunks


def process_document(
    pdf_path,
    vector_store_path
):

    print("Loading document...")

    pages = load_pdf(pdf_path)

    print(
        f"Pages extracted: {len(pages)}"
    )

    print("Creating chunks...")

    chunks = create_chunks(pages)

    print(
        f"Chunks created: {len(chunks)}"
    )

    # Extract chunk text
    chunk_texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print("Creating embeddings...")

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    embeddings = model.encode(
        chunk_texts,
        convert_to_numpy=True
    )

    print(
        f"Embeddings shape: {embeddings.shape}"
    )

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings)

    # Create cosine similarity index
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
       dimension
    )

    index.add(embeddings)

    print(
        f"Vectors stored: {index.ntotal}"
    )

    # Create directory
    vector_store_path = Path(
        vector_store_path
    )

    vector_store_path.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save index
    index_path = (
        vector_store_path
        / "research.index"
    )

    faiss.write_index(
        index,
        str(index_path)
    )

    # Save chunks
    chunks_path = (
        vector_store_path
        / "chunks.pkl"
    )

    with open(
        chunks_path,
        "wb"
    ) as f:

        pickle.dump(
            chunks,
            f
        )

    print(
        "\nDocument processed successfully!"
    )

    return {
        "pages": len(pages),
        "chunks": len(chunks),
        "index_path": index_path,
        "chunks_path": chunks_path
    }