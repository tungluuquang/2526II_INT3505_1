# app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

users = []

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data.get("name"):
        return jsonify({"error": "Name required"}), 400
    
    users.append(data)
    return jsonify(data), 201

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

if __name__ == "__main__":
    app.run(debug=True)