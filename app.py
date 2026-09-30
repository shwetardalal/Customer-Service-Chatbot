"""Flask web application for the customer-service chatbot."""

import logging

from flask import Flask, jsonify, render_template, request

from chatbot.classifier import IntentClassifier


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(MAX_MESSAGE_LENGTH=1000)
    if test_config:
        app.config.update(test_config)

    app.extensions["chatbot_classifier"] = IntentClassifier()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/chat")
    def chat():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify({"error": "Request body must be a JSON object."}), 400

        message = payload.get("message")
        if not isinstance(message, str):
            return jsonify({"error": "The 'message' field must be a string."}), 400

        message = message.strip()
        if not message:
            return jsonify({"error": "Please enter a message before sending."}), 400
        if len(message) > app.config["MAX_MESSAGE_LENGTH"]:
            return jsonify({
                "error": f"Messages must be {app.config['MAX_MESSAGE_LENGTH']} characters or fewer."
            }), 400

        try:
            result = app.extensions["chatbot_classifier"].predict(message)
        except Exception:
            app.logger.exception("Chatbot prediction failed")
            return jsonify({"error": "Sorry, something went wrong. Please try again."}), 500

        return jsonify(result)

    @app.errorhandler(413)
    def request_too_large(_error):
        return jsonify({"error": "The request is too large."}), 413

    return app


app = create_app()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
