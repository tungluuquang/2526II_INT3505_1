from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

def api_response(data=None, message="Success", status=200, error=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }), status

# Example
# false clarity

@app.route("/getUserInfo", methods=["GET"])
def get_user_info():
    return api_response(data=users)


@app.route("/makeUser", methods=["POST"])
def make_user():
    data = request.json

    new_user = {
        "id": len(users) + 1,
        "name": data.get("name")
    }

    users.append(new_user)

    return api_response(data=new_user, message="User created")


@app.route("/removeUser/<int:id>", methods=["DELETE"])
def remove_user(id):

    global users
    users = [u for u in users if u["id"] != id]

    return api_response(message="User removed")

# True clarity

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


@app.route("/api/v1/users", methods=["POST"])
def create_user():

    data = request.json

    if not data.get("name"):
        return api_response(
            message="Missing name",
            status=400,
            error="INVALID_INPUT"
        )

    new_user = {
        "id": len(users) + 1,
        "name": data["name"]
    }

    users.append(new_user)

    return api_response(
        data=new_user,
        message="User created",
        status=201
    )