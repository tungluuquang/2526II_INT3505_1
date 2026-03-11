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


# false — uppercase in URL
# URLs are case-sensitive and inconsistent

@app.route("/API/V1/Users", methods=["GET"])
def get_users_bad():
    return api_response(data=users)


# true — lowercase URL
# Recommended convention for REST APIs

@app.route("/api/v1/users", methods=["GET"])
def get_users_good():
    return api_response(data=users)