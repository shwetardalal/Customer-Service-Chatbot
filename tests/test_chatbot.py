"""Automated tests for chatbot intents and the Flask API."""

import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True})
    return app.test_client()


@pytest.mark.parametrize(
    ("message", "expected_intent"),
    [
        ("Hey, good morning", "greeting"),
        ("When are you open", "working_hours"),
        ("How much do your services cost", "pricing"),
        ("Can you explain the features", "product_info"),
        ("How do I check my order status", "order_status"),
        ("How do I get my money back", "refund"),
        ("How can I cancel my subscription", "cancellation"),
        ("I want to make a complaint", "complaint"),
        ("How can I reach a human agent", "contact"),
        ("Thanks for your help", "thanks"),
        ("See you later", "goodbye"),
    ],
)
def test_intent_classification(client, message, expected_intent):
    response = client.post("/chat", json={"message": message})
    assert response.status_code == 200
    result = response.get_json()
    assert result["intent"] == expected_intent
    assert result["reply"]
    assert 0.0 <= result["confidence"] <= 1.0


def test_unknown_question_uses_fallback(client):
    response = client.post("/chat", json={"message": "Explain the weather on Mars tomorrow"})
    assert response.status_code == 200
    result = response.get_json()
    assert result["intent"] == "fallback"
    assert result["reply"]


def test_classifier_preprocesses_question_variations(client):
    response = client.post("/chat", json={"message": "What time do you provide customer support?"})
    assert response.status_code == 200
    assert response.get_json()["intent"] == "working_hours"


def test_empty_message_is_rejected(client):
    response = client.post("/chat", json={"message": "   "})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_missing_message_is_rejected(client):
    response = client.post("/chat", json={})
    assert response.status_code == 400


def test_non_string_message_is_rejected(client):
    response = client.post("/chat", json={"message": 123})
    assert response.status_code == 400


def test_non_object_json_is_rejected(client):
    response = client.post("/chat", json=["hello"])
    assert response.status_code == 400


def test_oversized_message_is_rejected(client):
    response = client.post("/chat", json={"message": "x" * 1001})
    assert response.status_code == 400


def test_homepage_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Northstar support" in response.data
    assert b"chatMessages" in response.data


def test_chat_without_json_body_is_rejected(client):
    response = client.post("/chat", data="message=hello", content_type="text/plain")
    assert response.status_code == 400
