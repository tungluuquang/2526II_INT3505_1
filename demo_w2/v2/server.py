from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Tung"},
    {"id": 2, "name": "Nam"}
]

# home
@app.route("/")
def home():
    return "Flask server running"


# Resource identification
# /api/v2/users -> collection
@app.route("/api/v2/users", methods=["GET"])
def get_users():
    return jsonify(users)


# /api/v2/users/<id> -> specific resource
@app.route("/api/v2/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user)


# Manipulation through representations
# client gửi JSON để tạo resource
@app.route("/api/v2/users", methods=["POST"])
def create_user():
    data = request.get_json()

    new_user = {
        "id": len(users) + 1,
        "name": data["name"]
    }

    users.append(new_user)

    return jsonify(new_user), 201


# Self-descriptive messages
# response chứa status + message
@app.route("/api/v2/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return jsonify({
            "status": 404,
            "message": "User not found"
        }), 404

    users.remove(user)

    return jsonify({
        "status": 200,
        "message": "User deleted"
    })


# HATEOAS (hypermedia links)
@app.route("/api/v2/users/hateoas", methods=["GET"])
def users_with_links():

    result = []

    for u in users:
        result.append({
            "id": u["id"],
            "name": u["name"],
            "links": {
                "self": f"/api/v2/users/{u['id']}",
                "delete": f"/api/v2/users/{u['id']}"
            }
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)