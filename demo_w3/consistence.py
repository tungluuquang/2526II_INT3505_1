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
def api_response(data=None, message="Success", status=200, error=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }), status

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.query.get(user_id)
    if not user:
        return api_response(message="User not found", status=404, error="NOT_FOUND")
    return api_response(data=user.to_dict())

@app.route('/api/v1/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    return api_response(message="User deleted", status=200)
