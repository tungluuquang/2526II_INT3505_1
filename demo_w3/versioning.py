from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Alice", "status": "active", "email": "aliceinwonderland@gmail.com"},
    {"id": 2, "name": "Bob", "status": "inactive", "email": "bobbygang@gmail.com"},
    {"id": 3, "name": "Charlie", "status": "active", "email": "charlieputh@gmail.com"}
]

def api_response(data=None, message="Success", status=200, error=None):
    return jsonify({
        "status": status,
        "message": message,
        "data": data,
        "error": error
    }), status


# false — no versioning
# Any API change may break existing clients

@app.route("/api/users", methods=["GET"])
def users_no_version():
    return api_response(data=users)


# true — API version 1
# Original API response (no email)

@app.route("/api/v1/users", methods=["GET"])
def users_v1():

    users_v1_data = [
        {
            "id": u["id"],
            "name": u["name"],
            "status": u["status"]
        }
        for u in users
    ]

    return api_response(data=users_v1_data)


# true — API version 2
# Improved API with additional field (email)

@app.route("/api/v2/users", methods=["GET"])
def users_v2():

    users_v2_data = [
        {
            "id": u["id"],
            "name": u["name"],
            "status": u["status"],
            "email": u["email"]
        }
        for u in users
    ]

    return api_response(data=users_v2_data)

if __name__ == "__main__":
    app.run(debug=True)