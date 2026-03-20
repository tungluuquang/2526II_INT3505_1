from flask import Flask, jsonify, request
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
SECRET_KEY = "mysecretkey"

users = [
    {"id": 1, "name": "Tung", "password": "123"},
    {"id": 2, "name": "Nam",  "password": "456"}
]

# decorator 
def required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authorization header missing"}), 401
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user_id = payload["user_id"]   
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return wrapper

# routes 
@app.route("/api/v3/login", methods=["POST"])
def login():
    data     = request.get_json()
    name     = data.get("name")
    password = data.get("password")
    user = next(
        (u for u in users if u["name"] == name and u["password"] == password),
        None
    )
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    token = jwt.encode(
        {
            "user_id": user["id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return jsonify({"token": token})

@app.route("/api/v3/users", methods=["GET"])
@required                                          
def get_user():
    user = next((u for u in users if u["id"] == request.user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"id": user["id"], "name": user["name"]})

if __name__ == "__main__":
    app.run(debug=True)