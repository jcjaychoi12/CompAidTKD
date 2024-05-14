from flask import Flask, request
from db import *

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>CompAidTKD -- Backend</h1>"

@app.route('/competitors', methods=['GET', 'PUT', 'POST', 'DELETE'])
def competitors():
    args = request.args
    met = request.method

    if met == "GET":
        pass
    elif met == "POST":
        pass
    elif met == "PUT":
        pass
    elif met == "DELETE":
        pass

@app.route('/teams', methods=['GET', 'PUT', 'POST', 'DELETE'])
def teams():
    args = request.args
    met = request.method

    if met == "GET":
        pass
    elif met == "POST":
        pass
    elif met == "PUT":
        pass
    elif met == "DELETE":
        pass

@app.route('/matches', methods=['GET', 'PUT', 'POST', 'DELETE'])
def matches():
    args = request.args
    met = request.method

    if met == "GET":
        pass
    elif met == "POST":
        pass
    elif met == "PUT":
        pass
    elif met == "DELETE":
        pass

@app.route('/sparrings', methods=['GET', 'PUT', 'POST', 'DELETE'])
def sparrings():
    args = request.args
    met = request.method

    if met == "GET":
        pass
    elif met == "POST":
        pass
    elif met == "PUT":
        pass
    elif met == "DELETE":
        pass

@app.route('/poomsaes', methods=['GET', 'PUT', 'POST', 'DELETE'])
def poomsaes():
    args = request.args
    met = request.method

    if met == "GET":
        pass
    elif met == "POST":
        pass
    elif met == "PUT":
        pass
    elif met == "DELETE":
        pass


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000, debug=True)