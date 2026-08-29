import re


def create_chunks(
    pages,
    chunk_size=1200,
    chunk_overlap=200
):

    chunks = []

    for page in pages:

        text = page["text"]
        page_number = page["page_number"]

        # Clean excessive whitespace
        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        if not text:
            continue

        # Split into sentences
        sentences = re.split(
            r"(?<=[.!?])\s+",
            text
        )

        current_chunk = ""

        for sentence in sentences:

            sentence = sentence.strip()

            if not sentence:
                continue

            # If adding the sentence stays
            # within our chunk size
            if len(current_chunk) + len(sentence) + 1 <= chunk_size:

                current_chunk += (
                    " " + sentence
                ).strip()

            else:

                # Save current chunk
                if current_chunk:

                    chunks.append({
                        "text": current_chunk,
                        "page_number": page_number
                    })

                # Start new chunk
                current_chunk = sentence

        # Save remaining chunk
        if current_chunk:

            chunks.append({
                "text": current_chunk,
                "page_number": page_number
            })

    return chunks