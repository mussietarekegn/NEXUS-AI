
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT / "src" / "preprocessing")
)

from text_preprocessor import clean_text, tokenize_text


def test_lowercase():
    assert clean_text("HELLO WORLD") == "hello world"


def test_remove_punctuation():
    assert clean_text("Hello!!!") == "hello"


def test_remove_extra_spaces():
    assert clean_text("Hello     World") == "hello world"


def test_preserve_negation():
    assert "not" in clean_text("I am NOT happy")


def test_empty_input():
    assert clean_text(None) == ""


def test_tokenization():
    result = tokenize_text("Hello World")

    assert result == ["hello", "world"]


if __name__ == "__main__":

    test_lowercase()
    test_remove_punctuation()
    test_remove_extra_spaces()
    test_preserve_negation()
    test_empty_input()
    test_tokenization()

    print("All preprocessing tests passed!")
