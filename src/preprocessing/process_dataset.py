import pandas as pd

from pathlib import Path
from text_preprocessor import clean_text
from priority_labeler import assign_priority

RAW_PATH = Path("data/raw/support_tickets.csv")
PROCESSED_PATH = Path("data/processed/support_tikets_clean.csv")

df = pd.read_csv(RAW_PATH)

print("Original dataset size: ", len(df))

df = df.dropna(subset=["message"]).copy()

df["cleaned_message"] = df["message"].apply(clean_text)

df = df[df["cleaned_message"] != ""].copy()

df["priority"] = df["cleaned_message"].apply(assign_priority)

PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(PROCESSED_PATH, index=False)

print("\nPreprocessing completed!")
print("Processed dataset size:", len(df))

print("\nOriginal vs Cleaned messages:")

print(
    df[["message","cleaned_message"]].head(10)
)