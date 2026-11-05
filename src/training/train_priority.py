
import pandas as pd

from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score


df = pd.read_csv("data/processed/support_tikets_clean.csv")

X = df["cleaned_message"]
y = df["priority"]
groups = df["template_id"]


splitter = StratifiedGroupKFold(
    n_splits=4,
    shuffle=True,
    random_state=42
)

train_idx, test_idx = next(
    splitter.split(X, y, groups)
)

X_train = X.iloc[train_idx]
X_test = X.iloc[test_idx]

y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]


model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])


model.fit(X_train, y_train)


predictions = model.predict(X_test)

print("Priority Classification Accuracy:")
print(accuracy_score(y_test, predictions))

print("\nClassification Report:")
print(classification_report(y_test, predictions))


new_message = [
    "Someone hacked my account and stole my money"
]

prediction = model.predict(new_message)

print("\nNew message:", new_message[0])
print("Predicted priority:", prediction[0])
