from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTOR_DB_PATH = PROJECT_ROOT / "data" / "chroma_db"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_PATH)
)

collection = client.get_collection(
    name="nexus_knowledge"
)


query = "I cannot sign into my account"

query_embedding = model.encode(
    [query],
    normalize_embeddings=True
)

results = collection.query(
    query_embeddings=query_embedding.tolist(),
    n_results=min(3, collection.count())
)

print("Customer question:")
print(query)

print("\nRelevant knowledge-base results:")

for i in range(len(results["documents"][0])):

    document = results["documents"][0][i]

    metadata = results["metadatas"][0][i]

    distance = results["distances"][0][i]

    print(f"\nResult {i + 1}")
    print("Source:", metadata["source"])
    print("Chunk:", metadata["chunk_index"])
    print("Cosine distance:", round(distance, 4))
    print("Content:", document)
