from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice", "status": "active"},
    {"id": 2, "name": "Bob", "status": "inactive"},
    {"id": 3, "name": "Charlie", "status": "active"}
]

def api_response(data=None, message="Success", status=200, error=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }), status


# false — singular noun
# Does not clearly represent a collection resource

@app.route("/api/v1/user", methods=["GET"])
def get_user_list():
    return api_response(data=users)


@app.route("/api/v1/user/<int:user_id>", methods=["GET"])
def get_single_user(user_id):

    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return api_response(
            message="User not found",
            status=404,
            error="NOT_FOUND"
        )

    return api_response(data=user)


# true — plural noun
# Clearly represents a collection of users

@app.route("/api/v1/users", methods=["GET"])
def get_users():
    return api_response(data=users)


@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return api_response(
            message="User not found",
            status=404,
            error="NOT_FOUND"
        )

    return api_response(data=user)

if __name__ == "__main__":
    app.run(debug=True)