from flask import Flask, render_template_string, url_for

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Minimal Flask App</title>
</head>
<body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
    <h1>Hello from Flask!</h1>
    <img src="{{ url_for('static', filename='DevOps_testing_banner.png') }}" 
         alt="Sample Image" 
         style="max-width: 300px;">
    <p>This is a minimalistic Flask app running in Docker.</p>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
