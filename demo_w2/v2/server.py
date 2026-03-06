from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Tung"},
    {"id": 2, "name": "Nam"}
]

@app.route("/")
def home():
    return "Flask server running"

@app.route("/api/v2/users", methods=["GET"])
def get_users():
    return jsonify(users)

if __name__ == "__main__":
    app.run(debug=True)