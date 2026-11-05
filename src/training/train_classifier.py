import pandas as pd

from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/support_tikets_clean.csv")

X = df["cleaned_message"]
y = df["category"]
groups = df["template_id"]

splitter = StratifiedGroupKFold(
    n_splits=4,
    shuffle=True,
    random_state=42
)

train_indices, test_indices = next(
    splitter.split(X, y, groups)
)

X_train = X.iloc[train_indices]
X_test = X.iloc[test_indices]

y_train = y.iloc[train_indices]
y_test = y.iloc[test_indices]

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

train_groups = set(groups.iloc[train_indices])
test_groups = set(groups.iloc[test_indices])

print("Overlapping templates:", train_groups.intersection(test_groups))

models = {
    "Naive Bayes": Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", MultinomialNB())
    ]),

    "Logistic Regression": Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("classifier", LogisticRegression(max_iter=1000))
    ])
}

for model_name, model in models.items():
    print(model_name)

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("Accuracy:", round(accuracy, 4))

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    cm = confusion_matrix(
        y_test,
        predictions,
        labels=model.classes_
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=model.classes_
    )

    display.plot(xticks_rotation=45)
    plt.title(model_name)
    plt.tight_layout()
    plt.show()