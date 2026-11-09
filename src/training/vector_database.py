import sys
from pathlib import Path

# Add preprocessing directory to Python path
sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "preprocessing")
)

import chromadb
from sentence_transformers import SentenceTransformer
from document_chunker import split_into_chunks


PROJECT_ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_BASE = PROJECT_ROOT / "data" / "knowledge_base"

VECTOR_DB_PATH = PROJECT_ROOT / "data" / "chroma_db"


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_PATH)
)

collection = client.get_or_create_collection(
    name="nexus_knowledge",
    metadata={"hnsw:space": "cosine"}
)

documents = []
ids = []
metadatas = []

for file_path in KNOWLEDGE_BASE.glob("*.txt"):

    text = file_path.read_text(encoding="utf-8")

    chunks = split_into_chunks(
        text,
        chunk_size=120,
        overlap=30
    )

    for index, chunk in enumerate(chunks):

        document_id = f"{file_path.stem}_{index}"

        documents.append(chunk)

        ids.append(document_id)

        metadatas.append({
            "source": file_path.name,
            "chunk_index": index
        })


embeddings = model.encode(
    documents,
    normalize_embeddings=True
)

collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)


print("Knowledge base indexed successfully!")
print("Total chunks:", collection.count())
print("Vector database:", VECTOR_DB_PATH)
