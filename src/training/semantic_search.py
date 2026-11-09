from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

knowledge_base = [
    "How to reset your account password",
    "How to resolve failed credit card payments",
    "How to track a delayed delivery",
    "How to fix application crashes"
]

document_embeddings = model.encode(knowledge_base)

query = "I cannot sign into my account"

query_embedding = model.encode([query])

similarities = cosine_similarity(
    query_embedding,
    document_embeddings
)[0]

best_index = similarities.argmax()

print("Customer question:", query)

print("\nBest matching article:")
print(knowledge_base[best_index])

print("\nSimilarity score:")
print(round(float(similarities[best_index]), 4))
