import jwt
import datetime
from flask import Flask, request, jsonify
from functools import wraps
import os

app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-default-key")
ALGORITHM = "HS256"

USERS = [
    {
        "id": 1,
        "username": "admin",
        "password": "123456",
        "role": "admin",
        "scopes": ["read", "write", "delete", "admin"]
    },
    {
        "id": 2,
        "username": "user",
        "password": "123456",
        "role": "user",
        "scopes": ["read"]
    }
]

refresh_tokens = []

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "Thiếu token"}), 401

        try:
            parts = auth_header.split()
            if len(parts) != 2 or parts[0] != "Bearer":
                return jsonify({"message": "Header Authorization không hợp lệ"}), 401
            
            token = parts[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token đã hết hạn"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token không hợp lệ"}), 403

        return f(data, *args, **kwargs)

    return decorated

def scope_required(required_scopes):
    def decorator(f):
        @wraps(f)
        def decorated(user, *args, **kwargs):
            user_scopes = user.get("scopes", [])

            if not any(scope in user_scopes for scope in required_scopes):
                return jsonify({
                    "message": f"Thiếu quyền. Cần một trong các scope: {required_scopes}"
                }), 403

            return f(user, *args, **kwargs)
        return decorated
    return decorator

def role_required(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated(user, *args, **kwargs):
            user_role = user.get("role")

            if user_role not in required_roles:
                return jsonify({
                    "message": f"Không đủ quyền. Cần role: {required_roles}"
                }), 403

            return f(user, *args, **kwargs)
        return decorated
    return decorator

def generate_tokens(user):
    now = datetime.datetime.now(datetime.timezone.utc)
    
    payload = {
        "id": user["id"],
        "role": user["role"],
        "scopes": user["scopes"],
        "exp": now + datetime.timedelta(minutes=15)
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    refresh_payload = {
        "id": user["id"],
        "exp": now + datetime.timedelta(days=7)
    }
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

    return access_token, refresh_token

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    user = next((u for u in USERS if u["username"] == data.get("username") and u["password"] == data.get("password")), None)

    if not user:
        return jsonify({"message": "Sai tài khoản hoặc mật khẩu"}), 401

    access_token, refresh_token = generate_tokens(user)
    
    refresh_tokens.append(refresh_token)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token
    })

@app.route('/profile', methods=['GET'])
@token_required
def profile(user_data):
    return jsonify({
        "message": "Truy cập thành công",
        "user": user_data
    })

@app.route('/refresh-token', methods=['POST'])
def refresh():
    data = request.json
    token = data.get("refresh_token")

    if not token or token not in refresh_tokens:
        return jsonify({"message": "Refresh token không hợp lệ hoặc bị thiếu"}), 403

    try:
        user_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        if token in refresh_tokens:
            refresh_tokens.remove(token) 
        return jsonify({"message": "Refresh token đã hết hạn. Vui lòng đăng nhập lại."}), 403
    except jwt.InvalidTokenError:
        return jsonify({"message": "Refresh token không hợp lệ"}), 403

    user = next((u for u in USERS if u["id"] == user_data["id"]), None)
    if not user:
        return jsonify({"message": "Người dùng không còn tồn tại"}), 404

    now = datetime.datetime.now(datetime.timezone.utc)
    new_payload = {
        "id": user["id"],
        "role": user["role"], 
        "scopes": user["scopes"],
        "exp": now + datetime.timedelta(minutes=15)
    }

    new_access_token = jwt.encode(new_payload, SECRET_KEY, algorithm=ALGORITHM)

    return jsonify({"access_token": new_access_token})

@app.route('/books', methods=['GET'])
@token_required
@scope_required(["read"])
def get_books(user):
    return jsonify({"message": "Xem danh sách sách"})

@app.route('/logout', methods=['POST'])
def logout():
    token = request.json.get("refresh_token")

    if token in refresh_tokens:
        refresh_tokens.remove(token)

    return jsonify({"message": "Đăng xuất thành công"})

@app.route('/admin', methods=['GET'])
@token_required
@scope_required(["admin"])
@role_required(["admin"])
def admin_route(user):
    return jsonify({"message": "Chào mừng admin"})

@app.route('/admin-only', methods=['GET'])
@token_required
@role_required(["admin"])
def admin_only(user):
    return jsonify({"message": "Chỉ admin"})

    
if __name__ == '__main__':
    app.run(debug=True)