from flask import Flask
from db import *

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>CompAidTKD -- Backend</h1>"

@app.route('/competitors')
def competitors():
    return "Competitors"

@app.route('/teams')
def teams():
    return "Teams"

@app.route('/matches')
def matches():
    return "Matches"

@app.route('/sparrings')
def sparrings():
    return "Sparrings"

@app.route('/poomsaes')
def poomsaes():
    return "Poomsaes"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)