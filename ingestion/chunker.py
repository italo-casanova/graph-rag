def chunk_text(text, size=500):

    chunks = []

    start = 0

    while start < len(text):

        chunks.append(text[start : start + size])

        start += size

    return chunks
