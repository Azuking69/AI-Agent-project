from flask import Flask, render_template
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel


load_dotenv()
app = Flask(__name__)
anthropic = Anthropic()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)