from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env (for local dev)

app = Flask(__name__)

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")  # This will work on Render too
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
    
    translations = {}
    for lang in target_langs:
        if source_lang != lang:  # skip translating to the same language
            response = requests.post(
                "https://api-free.deepl.com/v2/translate",
                data={
                    "auth_key": DEEPL_API_KEY,
                    "text": text,
                    "target_lang": lang,
                    "source_lang": source_lang if source_lang != "auto" else None
                }
            )
            if response.ok:
                translated_text = response.json()["translations"][0]["text"]
                translations[lang] = translated_text
            else:
                translations[lang] = f"Error: {response.status_code}"

    return jsonify(translations)

if __name__ == "__main__":
    app.run(debug=True)
