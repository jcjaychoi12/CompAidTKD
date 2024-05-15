from flask import Flask, request, jsonify
from db import *

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>CompAidTKD -- Backend</h1>"

@app.route('/competitors', methods=['GET', 'POST', 'PUT', 'DELETE'])
def competitors():
    args = request.args
    met = request.method

    if met == "GET":
        if "id" not in args:
            return jsonify({"message": "Error: valid id not found"}), 400
        try:
            get_result = Competitors.get_Competitor(int(args.get("id")))
            return jsonify(get_result)
        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"}), 500
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