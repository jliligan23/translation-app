from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env (for local dev)

app = Flask(__name__)

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")  # Same key, no need to regenerate
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text")
    source_lang = data.get("source_lang", "auto")
    target_langs = ["en", "nl", "fr", "de", "es"]

    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    translations = {}

    for lang in target_langs:
        if source_lang != lang:  # skip same-language translation
            payload = {
                "text": text,
                "target_lang": lang.upper()
            }

            if source_lang != "auto":
                payload["source_lang"] = source_lang.upper()

            response = requests.post(
                DEEPL_API_URL,
                headers=headers,
                data=payload
            )

            if response.ok:
                translated_text = response.json()["translations"][0]["text"]
                translations[lang] = translated_text
            else:
                translations[lang] = f"Error {response.status_code}: {response.text}"

    return jsonify(translations)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render or local
    app.run(host="0.0.0.0", port=port)
