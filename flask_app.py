"""Flask: Hello World and a Bootstrap page (exercises 1 and 5)."""

from flask import Flask, render_template

app = Flask(__name__)


@app.get("/hello")
def hello():
    return "Привет Flask!"


@app.get("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)
