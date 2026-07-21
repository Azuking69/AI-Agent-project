import flask
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel


app = flask.Flask(__name__)
load_dotenv()
anthropic = Anthropic()

@app.route("/", methods=["GET"])
def index():
    return flask.render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port="5000")