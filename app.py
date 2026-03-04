from flask import Flask, render_template, url_for
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Read the header from the env var provided in Dockerfile, or in K8s cfgmap 
    message = os.getenv("CUSTOM_HEADER", "Default header")
    
    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
