from flask import Flask, render_template, url_for
import os

app = Flask(__name__)


def read_message_from_config(path: str) -> str | None:
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                return fh.read().strip()
    except Exception:
        pass
    return None


@app.route("/")
def index():
    # Prefer a mounted ConfigMap file (CONFIG_PATH). Fall back to env MESSAGE for local runs.
    config_path = os.environ.get("CONFIG_PATH", "/etc/config/CUSTOM_HEADER")
    message = read_message_from_config(config_path) or os.environ.get("MESSAGE", "Hello from Flask!")
    return render_template("index.html", message=message)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
