def split_into_chunks(text, chunk_size=120, overlap=30):
    
    words = text.split()

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk_words = words[start:end]

        chunk_text = " ".join(chunk_words)

        chunks.append(chunk_text)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


if __name__ == "__main__":

    sample_text = """
    Password recovery is important.
    Customers can reset passwords through their email.
    Payment problems should be reported to billing support.
    Delivery tracking is available using an order number.
    """

    results = split_into_chunks(
        sample_text,
        chunk_size=15,
        overlap=5
    )

    for i in range(len(results)):
        print(f"\nChunk {i + 1}:")
        print(results[i])
