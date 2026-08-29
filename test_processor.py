from pathlib import Path

from src.document_processor import process_document


project_root = Path(__file__).resolve().parent

pdf_path = (
    project_root
    / "data"
    / "papers"
    / "attention_is_all_you_need.pdf"
)

vector_store_path = (
    project_root
    / "data"
    / "test_vector_store"
)


result = process_document(
    pdf_path,
    vector_store_path
)


print("\n==============================")
print("Processing Summary")
print("==============================")

print(
    f"Pages: {result['pages']}"
)

print(
    f"Chunks: {result['chunks']}"
)

print(
    f"Index: {result['index_path']}"
)

print(
    f"Chunks file: {result['chunks_path']}"
)