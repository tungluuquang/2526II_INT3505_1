from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

# example consistency

# False, naming endpoints and response 
@app.route("/getUsers", methods=["GET"])
def get_users():
    return jsonify({
        "data": users
    })
 
@app.route('/delete')      
def delete():
    users.pop()
    return "Deleted"     


# True, naming endpoints and response
def api_response(data=None, message="Success", status=200, error=None, pagination=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data,
        "error": error,
        "pagination": pagination
    }), status


# NEW: pagination endpoint
@app.route('/api/v1/users', methods=['GET'])
def get_users_paginated():

    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=2, type=int)

    start = (page - 1) * limit
    end = start + limit

    paginated_users = users[start:end]

    pagination = {
        "page": page,
        "limit": limit,
        "total": len(users),
        "total_pages": (len(users) + limit - 1) // limit
    }

    return api_response(data=paginated_users, pagination=pagination)


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)    
    if not user:
        return api_response(message="User not found", status=404, error="NOT_FOUND")
    return api_response(data=user)


@app.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    global users

    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return api_response(
            message="User not found",
            status=404,
            error="NOT_FOUND"
        )

    users = [u for u in users if u["id"] != user_id]

    return api_response(message="User deleted", status=200)


if __name__ == "__main__":
    app.run(debug=True)