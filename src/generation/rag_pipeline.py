
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[2]

VECTOR_DB_PATH = PROJECT_ROOT / "data" / "chroma_db"

load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=str(VECTOR_DB_PATH)
)

collection = client.get_collection(
    name="nexus_knowledge"
)

gemini_client = genai.Client(
    api_key=api_key
)

def retrieve_documents(question, number_of_results=3):

    total_documents = collection.count()

    if total_documents == 0:
        return []

    question_embedding = embedding_model.encode(
        [question],
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=min(number_of_results, total_documents)
    )

    retrieved_documents = []

    for i in range(len(results["documents"][0])):

        document = results["documents"][0][i]

        metadata = results["metadatas"][0][i]

        distance = results["distances"][0][i]

        retrieved_documents.append({
            "content": document,
            "source": metadata["source"],
            "distance": distance
        })

    return retrieved_documents

def generate_answer(question, retrieved_documents):

    if not retrieved_documents:
        return "I could not find relevant information in the knowledge base."

    context = ""

    for i in range(len(retrieved_documents)):

        document = retrieved_documents[i]

        context += (
            f"\nSource: {document['source']}\n"
            f"Content: {document['content']}\n"
        )

    prompt = f"""
You are NEXUS AI, a helpful customer support assistant.

Your task is to answer the customer's question using
only the supplied knowledge-base context.

Rules:
1. Do not invent information.
2. Do not make up company policies or procedures.
3. If the context does not answer the question,
   clearly say that you do not have enough information.
4. Give clear, polite, practical answers.
5. Mention the source filenames you used.

KNOWLEDGE BASE CONTEXT:
{context}

CUSTOMER QUESTION:
{question}

YOUR ANSWER:
"""

    response = gemini_client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    if not response.text:
        return "I could not generate an answer. Please try again."

    return response.text

def ask_nexus(question):

    retrieved_documents = retrieve_documents(question)

    answer = generate_answer(
        question,
        retrieved_documents
    )

    return {
        "question": question,
        "answer": answer,
        "sources": [
            document["source"]
            for document in retrieved_documents
        ]
    }

if __name__ == "__main__":

    question = "I cannot sign into my account. How can I fix it?"

    result = ask_nexus(question)

    print("\nCUSTOMER QUESTION:")
    print(result["question"])

    print("\nNEXUS AI ANSWER:")
    print(result["answer"])

    print("\nSOURCES:")
    for source in result["sources"]:
        print("-", source)
