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


# false — using underscore

@app.route("/api/v1/user_profiles", methods=["GET"])
def get_profiles_bad():

    profiles = [
        {"id": 1, "user_id": 1, "bio": "Developer"}
    ]

    return api_response(data=profiles)


# false — using camelCase

@app.route("/api/v1/userProfiles", methods=["GET"])
def get_profiles_bad2():
    return api_response(data=[])


# true — using hyphens

@app.route("/api/v1/user-profiles", methods=["GET"])
def get_profiles():

    profiles = [
        {"id": 1, "user_id": 1, "bio": "Developer"}
    ]

    return api_response(data=profiles)

if __name__ == "__main__":
    app.run(debug=True)