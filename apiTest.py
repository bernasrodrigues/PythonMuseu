from flask import Flask

app = Flask(__name__)

# API super simples
@app.route("/")
def hello():
    # Returna texto (url)
    return "www.google.com"


if __name__ == "__main__":
    app.run(debug=True)
