from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database
users = [
    {"id": 1, "name": "Nguyen Van A", "email": "nguyenvana@example.com"},
    {"id": 2, "name": "Tran Thi B", "email": "tranthib@example.com"},
    {"id": 3, "name": "Le Van C", "email": "levanc@example.com"},
]
next_id = 4


# GET /users - Lấy tất cả users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({
        "success": True,
        "count": len(users),
        "data": users
    }), 200


# GET /users/<id> - Lấy user theo ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return jsonify({
            "success": False,
            "message": f"User with id {user_id} not found"
        }), 404

    return jsonify({
        "success": True,
        "data": user
    }), 200


# POST /users - Tạo user mới
@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "success": False,
            "message": "Name and email are required"
        }), 400

    if any(u["email"] == email for u in users):
        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 409

    new_user = {
        "id": next_id,
        "name": name,
        "email": email
    }

    users.append(new_user)
    next_id += 1

    return jsonify({
        "success": True,
        "message": "User created successfully",
        "data": new_user
    }), 201


# PUT /users/<id> - Cập nhật user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return jsonify({
            "success": False,
            "message": f"User with id {user_id} not found"
        }), 404

    email = data.get("email")

    if email and email != user["email"]:
        if any(u["email"] == email for u in users):
            return jsonify({
                "success": False,
                "message": "Email already exists"
            }), 409

    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])

    return jsonify({
        "success": True,
        "message": "User updated successfully",
        "data": user
    }), 200


# DELETE /users/<id> - Xóa user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users

    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        return jsonify({
            "success": False,
            "message": f"User with id {user_id} not found"
        }), 404

    users = [u for u in users if u["id"] != user_id]

    return jsonify({
        "success": True,
        "message": "User deleted successfully",
        "data": user
    }), 200


if __name__ == '__main__':
    app.run(port=3000, debug=True)