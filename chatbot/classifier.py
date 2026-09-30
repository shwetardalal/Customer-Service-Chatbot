"""TF-IDF and cosine-similarity based intent classifier."""

import json
import random
from pathlib import Path
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from chatbot.preprocess import preprocess_text


class IntentClassifier:
    """Match a user message to the closest intent training example."""

    def __init__(self, intents_path: str | Path | None = None, threshold: float = 0.62):
        self.intents_path = Path(intents_path) if intents_path else Path(
            __file__).with_name("intents.json")
        self.threshold = threshold
        self.intents = self._load_intents()
        self.responses = {item["tag"]: item["responses"]
                          for item in self.intents}
        self.fallback_responses = self.responses["fallback"]

        self.training_texts: list[str] = []
        self.training_tags: list[str] = []
        for intent in self.intents:
            if intent["tag"] == "fallback":
                continue
            for pattern in intent["patterns"]:
                self.training_texts.append(pattern)
                self.training_tags.append(intent["tag"])

        self.vectorizer = TfidfVectorizer(
            preprocessor=preprocess_text,
            tokenizer=str.split,
            token_pattern=None,
            lowercase=False,
            ngram_range=(1, 2),
            sublinear_tf=True,
        )
        self.training_vectors = self.vectorizer.fit_transform(
            self.training_texts)

    def _load_intents(self) -> list[dict[str, Any]]:
        """Load and minimally validate the intent data file."""
        try:
            data = json.loads(self.intents_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(
                f"Could not load chatbot intents from {self.intents_path}") from error

        intents = data.get("intents") if isinstance(data, dict) else None
        if not isinstance(intents, list):
            raise ValueError(
                "The intents file must contain an 'intents' list.")
        tags = {item.get("tag") for item in intents if isinstance(item, dict)}
        if "fallback" not in tags:
            raise ValueError("The intents file must define a fallback intent.")
        for item in intents:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("tag"), str)
                or not isinstance(item.get("patterns"), list)
                or not isinstance(item.get("responses"), list)
                or not item["responses"]
            ):
                raise ValueError(
                    "Each intent must have a tag, patterns list, and responses list.")
        return intents

    def predict(self, message: str) -> dict[str, Any]:
        """Return the response, matched intent, and cosine-similarity confidence."""
        if not isinstance(message, str) or not message.strip():
            raise ValueError("Message must be a non-empty string.")

        message_vector = self.vectorizer.transform([message])
        scores = cosine_similarity(
            message_vector, self.training_vectors).ravel()
        best_index = int(scores.argmax())
        confidence = float(scores[best_index])
        predicted_tag = self.training_tags[best_index]

        if confidence < self.threshold:
            predicted_tag = "fallback"
            response = random.choice(self.fallback_responses)
        else:
            response = random.choice(self.responses[predicted_tag])

        return {
            "reply": response,
            "intent": predicted_tag,
            "confidence": round(confidence, 4),
        }
