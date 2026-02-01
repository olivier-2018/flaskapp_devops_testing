from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Read the header from the Kubernetes ConfigMap mounted at /etc/config/CUSTOM_HEADER.
    # Do not read from an env var; fall back only to a sensible default.
    message = os.getenv("CUSTOM_HEADER", "Default header")
    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
