import re
import string

def clean_text(text):

    if not isinstance(text, str):
        return ""

    text = text.lower()

    text = text.translate(str.maketrans("","",string.punctuation))

    text = re.sub(r"\s+"," ",text)

    text = text.strip()

    return text

def tokenize_text(text):

    cleaned_text = clean_text(text)

    tokens = cleaned_text.split()

    return tokens

if __name__ == "__main__":

    message = "  HELLO!!! I CANNOT LOGIN TO MY ACCOUNT!!!   "

    cleaned = clean_text(message)

    tokens = tokenize_text(message)

    print("orginal message: ")
    print(message)

    print("\nCleaned message:")
    print(cleaned)

    print("\nTokens:")
    print(tokens)
