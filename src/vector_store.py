from pathlib import Path
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# ---------------------------------
# Load embedding model
# ---------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_vector_store(
    chunks,
    vector_store_path
):

    vector_store_path = Path(
        vector_store_path
    )

    # Create directory if it doesn't exist
    vector_store_path.mkdir(
        parents=True,
        exist_ok=True
    )

    # ---------------------------------
    # Extract text from chunks
    # ---------------------------------

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    # ---------------------------------
    # Create embeddings
    # ---------------------------------

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    # Convert to float32
    embeddings = embeddings.astype(
        "float32"
    )

    # ---------------------------------
    # Normalize embeddings
    # ---------------------------------

    faiss.normalize_L2(
        embeddings
    )

    # ---------------------------------
    # Create FAISS index
    # ---------------------------------

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    # ---------------------------------
    # Add embeddings to FAISS
    # ---------------------------------

    index.add(
        embeddings
    )

    # ---------------------------------
    # Save FAISS index
    # ---------------------------------

    index_path = (
        vector_store_path
        / "research.index"
    )

    faiss.write_index(
        index,
        str(index_path)
    )

    # ---------------------------------
    # Save chunks
    # ---------------------------------

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
        f"Vector store created successfully."
    )

    print(
        f"Chunks: {len(chunks)}"
    )

    print(
        f"Embedding dimension: {dimension}"
    )

    print(
        f"Vector store: {vector_store_path}"
    )


# ---------------------------------
# Local testing
# ---------------------------------

if __name__ == "__main__":

    project_root = (
        Path(__file__).resolve().parent.parent
    )

    print(
        "vector_store.py is ready."
    )