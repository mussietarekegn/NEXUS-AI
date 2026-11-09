from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "I cannot access my account",
    "I am unable to sign in",
    "My payment was declined",
    "My credit card transaction failed",
    "Where is my delivery package?"
]

embeddings = model.encode(sentences)

print("Number of sentences:", len(sentences))
print("Embedding shape:", embeddings.shape)

similarities = cosine_similarity(
    [embeddings[0]],
    embeddings
)[0]

print("\nSimilarity with the first sentence:")

for i in range(len(sentences)):
    print(
        sentences[i],
        "->",
        round(float(similarities[i]), 4)
    )
