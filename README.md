# Customer Service Chatbot

A local customer-service chatbot built with Flask and traditional NLP. It classifies a message against example utterances using NLTK text preprocessing, scikit-learn TF-IDF vectors, and cosine similarity. It does not call paid APIs or use an LLM.

## Features

- Recognizes greetings, working hours, pricing, product information, order status, refunds, cancellations, complaints, contact questions, thanks, and goodbyes.
- Uses a configurable cosine-similarity confidence threshold and a friendly fallback for unsupported questions.
- Provides a responsive chat page with message bubbles, suggested prompts, a typing indicator, clear-chat control, and Enter-to-send support.
- Validates API requests and returns useful JSON errors for invalid input.
- Includes automated tests for every supported intent and the HTTP endpoints.

## Technologies

Python, Flask, NLTK, scikit-learn, HTML, CSS, JavaScript, JSON, and pytest.

## Project structure

```text
customer-service-chatbot/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── chatbot/
│   ├── __init__.py
│   ├── preprocess.py
│   ├── classifier.py
│   └── intents.json
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── tests/
    └── test_chatbot.py
```

## Installation

Use Python 3.10 or newer. Open this project folder in VS Code, then create and activate a virtual environment from its integrated terminal.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks environment activation, use the interpreter directly as `.venv\Scripts\python.exe` for the install, run, and test commands below.

In VS Code, select `.venv\Scripts\python.exe` with **Python: Select Interpreter**. The project also includes a workspace setting to suggest this interpreter.

### NLTK resources

The app uses NLTK's bundled Treebank tokenizer, so tokenization works without downloading tokenizer data. It attempts to use NLTK's English stop-word corpus and automatically falls back to a small built-in list if the corpus is missing. To install the full corpus for this Python environment, run:

```powershell
python -m nltk.downloader stopwords
```

You can also download it from Python with `import nltk; nltk.download("stopwords")`. Some restricted or proxied networks may block NLTK corpus downloads; this project remains fully usable with its built-in stop-word fallback. No API keys or other secrets are needed.

## Run the application

From the project directory with the virtual environment active:

```powershell
python app.py
```

Open `http://127.0.0.1:5000` in a browser. The Flask development server is for local development; deploy behind a production WSGI server for public use.

## API

`POST /chat` accepts JSON containing a non-empty `message` string (up to 1,000 characters):

```json
{"message": "When are you open?"}
```

A successful response includes the selected `intent`, a `reply`, and a cosine-similarity `confidence` score. Invalid requests return a JSON `error` and an appropriate HTTP 4xx status.

## Tests

Run the test suite from the project folder:

```powershell
python -m pytest -q
```

## Example questions

- “What are your working hours?”
- “How much do your services cost?”
- “Can you explain the features?”
- “Can I track my package?”
- “How do I get a refund?”
- “How can I cancel my subscription?”
- “I want to make a complaint.”
- “How can I reach a human agent?”
- “Thanks for your help!”
- “Goodbye!”

Add or edit patterns and responses in `chatbot/intents.json` to adapt the bot to your organization. The similarity threshold is configured in `IntentClassifier` in `chatbot/classifier.py`.
