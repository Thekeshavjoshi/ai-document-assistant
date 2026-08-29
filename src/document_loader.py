import pymupdf


def load_pdf(pdf_path):

    document = pymupdf.open(pdf_path)

    pages = []

    print(f"Total pages: {len(document)}")

    for page_number, page in enumerate(document):

        text = page.get_text()

        pages.append({
            "page_number": page_number + 1,
            "text": text
        })

    document.close()

    return pages