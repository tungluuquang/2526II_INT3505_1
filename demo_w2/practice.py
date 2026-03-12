from flask import Flask, jsonify, request

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


# get
@app.route("/api/v1/users", methods=["GET"])
def get_users():
    return api_response(data=users)


# post
@app.route("/api/v1/users", methods=["POST"])
def create_user():
    body = request.get_json()

    if not body:
        return api_response(
            message="Invalid request body",
            status=400,
            error="Request body is missing"
        )

    if "name" not in body or "status" not in body:
        return api_response(
            message="Missing required fields",
            status=400,
            error="name and status are required"
        )

    new_user = {
        "id": len(users) + 1,
        "name": body["name"],
        "status": body["status"]
    }

    users.append(new_user)

    return api_response(
        data=new_user,
        message="User created",
        status=201
    )


# put
@app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    body = request.get_json()

    for user in users:
        if user["id"] == user_id:

            if "name" not in body or "status" not in body:
                return api_response(
                    message="Missing required fields",
                    status=400,
                    error="name and status are required"
                )

            user["name"] = body["name"]
            user["status"] = body["status"]

            return api_response(
                data=user,
                message="User updated",
                status=200
            )

    return api_response(
        message="User not found",
        status=404,
        error="User does not exist"
    )


# patch
@app.route("/api/v1/users/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    body = request.get_json()

    for user in users:
        if user["id"] == user_id:

            if "name" in body:
                user["name"] = body["name"]

            if "status" in body:
                user["status"] = body["status"]

            return api_response(
                data=user,
                message="User partially updated",
                status=200
            )

    return api_response(
        message="User not found",
        status=404,
        error="User does not exist"
    )


# delete
@app.route("/api/v1/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)

            return api_response(
                message="User deleted",
                status=200
            )

    return api_response(
        message="User not found",
        status=404,
        error="User does not exist"
    )

@app.route("/api/v1/error", methods=["GET"])
def trigger_error():
    return api_response(
        message="Internal Server Error",
        status=500,
        error="Something went wrong on the server"
    )


if __name__ == "__main__":
    app.run(debug=True)