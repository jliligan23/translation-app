# main.py  – desktop launcher
import threading
import webview

# 1) import your existing Flask app
from app import app          # <- this is the same app object defined in app.py

# 2) run Flask in a background thread so it doesn't block the window
def run_flask():
    # turn off the reloader (it interferes with threads)
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()

    # 3) create the desktop window
    webview.create_window(
        title="Multi-Language Translator",
        url="http://127.0.0.1:5000",
        width=1200,
        height=800,
        resizable=True,
    )
    webview.start()
