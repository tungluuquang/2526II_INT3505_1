from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Tung"},
    {"id": 2, "name": "Nam"}
]

# stateless
@app.route("/")
def home():
    return "Flask server running"

@app.route("/api/v3/users", methods=["GET"])
def get_user():
    user_id = request.headers.get("X-User-ID")

    if not user_id:
        return jsonify({"error": "User ID header missing"}), 400

    user = next((u for u in users if u["id"] == int(user_id)), None)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)

if __name__ == "__main__":
    app.run(debug=True)