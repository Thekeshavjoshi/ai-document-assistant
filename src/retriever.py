from pathlib import Path
import pickle

import faiss
from sentence_transformers import SentenceTransformer


# ---------------------------------
# Load embedding model
# ---------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def retrieve(
    query,
    vector_store_path,
    top_k=8
):

    vector_store_path = Path(
        vector_store_path
    )

    index_path = (
        vector_store_path
        / "research.index"
    )

    chunks_path = (
        vector_store_path
        / "chunks.pkl"
    )

    # ---------------------------------
    # Load FAISS index
    # ---------------------------------

    index = faiss.read_index(
        str(index_path)
    )

    # ---------------------------------
    # Load chunks
    # ---------------------------------

    with open(
        chunks_path,
        "rb"
    ) as f:

        chunks = pickle.load(f)

    if not chunks:
        return []

    # ---------------------------------
    # Create query embedding
    # ---------------------------------

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    # ---------------------------------
    # Normalize query embedding
    # ---------------------------------

    faiss.normalize_L2(
        query_embedding
    )

    # ---------------------------------
    # FAISS search
    # ---------------------------------

    # The document vectors were created
    # using IndexFlatIP after normalization.
    #
    # Therefore, the returned inner-product
    # score is directly the cosine similarity.

    actual_top_k = min(
        top_k,
        len(chunks)
    )

    distances, indices = index.search(
        query_embedding,
        actual_top_k
    )

    results = []

    # ---------------------------------
    # Similarity threshold
    # ---------------------------------

    SIMILARITY_THRESHOLD = 0.35

    # ---------------------------------
    # Convert FAISS score directly
    # to cosine similarity
    # ---------------------------------

    for distance, index_position in zip(
        distances[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        # IndexFlatIP + normalized vectors
        # means inner product = cosine similarity.
        similarity = float(distance)

        if similarity < SIMILARITY_THRESHOLD:
            continue

        chunk = chunks[index_position]

        results.append({
            "text": chunk["text"],
            "page_number": chunk["page_number"],
            "similarity": similarity
        })

    # ---------------------------------
    # Rerank results
    #
    # Highest similarity first
    # ---------------------------------

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results


# ---------------------------------
# Local testing
# ---------------------------------

if __name__ == "__main__":

    project_root = (
        Path(__file__).resolve().parent.parent
    )

    vector_store_path = (
        project_root
        / "data"
        / "test_vector_store"
    )

    query = (
        "What is multi-head attention?"
    )

    results = retrieve(
        query,
        vector_store_path,
        top_k=8
    )

    print(
        f"\nRetrieved {len(results)} "
        f"relevant chunks."
    )

    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\n--- Result {i} ---"
        )

        print(
            f"Page: "
            f"{result['page_number']}"
        )

        print(
            f"Cosine similarity: "
            f"{result['similarity']:.4f}"
        )

        print(
            result["text"][:500]
        )
