from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

documents = [
    "I love python",
    "I love machine learning",
    "Python is intersting"
]

print("BAY OF WORDS")

bow_vectorizer = CountVectorizer()

bow_matrix = bow_vectorizer.fit_transform(documents)

print("Vocabulary: ")
print(bow_vectorizer.get_feature_names_out())

print("\nNumerical representation: ")
print(bow_matrix.toarray())

print("\n TF-IDF")

tfidf_vectorizer = TfidfVectorizer()

tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

print("Vocabulary: ")
print(tfidf_vectorizer.get_feature_names_out())

print("\nTF-IDF representaion: ")
print(tfidf_matrix.toarray())
