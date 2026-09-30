"""Small, offline-friendly text preprocessing helpers built with NLTK."""

import re
from functools import lru_cache

from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer

# Used if the optional NLTK stopwords corpus has not been downloaded.
_FALLBACK_STOP_WORDS = frozenset(
    "a an and are as at be been being but by can could did do does doing for from "
    "had has have having he her hers him his how i if in into is it its me my of "
    "on or our ours she so than that the their theirs them then there these they "
    "this those to was we were what when where which who why will with you your yours"
    .split()
) - {"no", "not", "nor", "never"}
_TOKENIZER = TreebankWordTokenizer()


@lru_cache(maxsize=1)
def get_stop_words() -> frozenset[str]:
    """Load NLTK's English stop words, with a small offline fallback."""
    try:
        return frozenset(stopwords.words("english")) - {"no", "not", "nor", "never"}
    except LookupError:
        return _FALLBACK_STOP_WORDS


def tokenize(text: str) -> list[str]:
    """Lowercase and tokenize text using NLTK's bundled Treebank tokenizer."""
    return [
        token.lower()
        for token in _TOKENIZER.tokenize(text)
        if re.search(r"[a-z0-9]", token, flags=re.IGNORECASE)
    ]


def preprocess_text(text: str) -> str:
    """Normalize text and remove unhelpful stop words while preserving negation."""
    tokens = tokenize(text)
    stop_words = get_stop_words()
    return " ".join(token for token in tokens if token not in stop_words)
