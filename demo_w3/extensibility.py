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

# Example
# false case

@app.route("/api/v1/getActiveUsers", methods=["GET"])
def get_active_users():
    active_users = [u for u in users if u["status"] == "active"]
    return api_response(data=active_users)


@app.route("/api/v1/getInactiveUsers", methods=["GET"])
def get_inactive_users():
    inactive_users = [u for u in users if u["status"] == "inactive"]
    return api_response(data=inactive_users)

# true case

@app.route("/api/v1/users", methods=["GET"])
def get_users():

    status = request.args.get("status")

    filtered_users = users

    if status:
        filtered_users = [u for u in users if u["status"] == status]

    return api_response(data=filtered_users)