"""
OAuth 2.0 Authorization Code Grant — Flask Demo
================================================
Mô phỏng đầy đủ 5 bước: cả Client App lẫn Authorization Server
đều chạy trên cùng một process để dễ quan sát.

Chạy:  python app.py
Mở:    http://localhost:5000
"""

import os, secrets, hashlib, base64, time, json
from functools import wraps
from urllib.parse import urlencode, urlparse, parse_qs

from flask import (Flask, request, redirect, url_for,
                   session, render_template, abort, jsonify, g)

app = Flask(__name__)
app.secret_key = "demo-secret-key-DO-NOT-USE-IN-PROD"

REGISTERED_CLIENTS = {
    "my-flask-client": {
        "client_secret": "super-secret",
        "redirect_uris": ["http://localhost:5000/callback"],
        "scopes": ["profile", "email"],
        "name": "Flask Demo App",
    }
}

USERS = {
    "alice": {"password": "1234", "email": "alice@example.com", "name": "Alice Nguyen"},
    "bob":   {"password": "5678", "email": "bob@example.com",   "name": "Bob Tran"},
}

# In-memory stores
AUTH_CODES   = {}   # code  → {client_id, redirect_uri, user, scopes, expires}
ACCESS_TOKENS = {}  # token → {client_id, user, scopes, expires}

# Helper: sinh token ngẫu nhiên
def gen_token(n=32):
    return secrets.token_urlsafe(n)

def b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()

# CLIENT APP  

# Bước 1: User vào /login
@app.route("/")
def index():
    user_info = session.get("user_info")
    return render_template("index.html", user_info=user_info,
                           steps=session.get("steps", []))

@app.route("/login")
def login():
    """BƯỚC 1 — Tạo Authorization Request, redirect tới Auth Server."""
    state  = gen_token(16)            
    nonce  = gen_token(16)
    session["oauth_state"] = state
    session["steps"] = []             

    _log_step(1, "Client tạo state, redirect tới /authorize",
              f"state={state[:8]}…  scope=profile email")

    params = {
        "client_id":     "my-flask-client",
        "redirect_uri":  "http://localhost:5000/callback",
        "response_type": "code",
        "scope":         "profile email",
        "state":         state,
        "nonce":         nonce,
    }
    auth_url = "http://localhost:5000/oauth/authorize?" + urlencode(params)
    return redirect(auth_url)


# Bước 3: Auth Server gọi về đây
@app.route("/callback")
def callback():
    """BƯỚC 3 — Nhận Authorization Code từ Auth Server."""
    code  = request.args.get("code")
    state = request.args.get("state")
    error = request.args.get("error")

    if error:
        return render_template("error.html", msg=f"Auth Server trả lỗi: {error}")

    if state != session.pop("oauth_state", None):
        return render_template("error.html", msg="State không khớp — có thể bị CSRF!")

    _log_step(3, "Nhận Authorization Code từ callback URL",
              f"code={code[:8]}…  state đã xác minh ✓")

    # Bước 4: Đổi code → Access Token
    _log_step(4, "POST /oauth/token để đổi code → access_token",
              "Gửi kèm client_secret (server-to-server, user không thấy)")

    import urllib.request
    payload = urlencode({
        "grant_type":    "authorization_code",
        "code":          code,
        "redirect_uri":  "http://localhost:5000/callback",
        "client_id":     "my-flask-client",
        "client_secret": "super-secret",
    }).encode()

    req = urllib.request.Request(
        "http://localhost:5000/oauth/token",
        data=payload,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req) as r:
        token_data = json.loads(r.read())

    access_token = token_data["access_token"]
    session["access_token"] = access_token
    _log_step(4, "Nhận được access_token ✓",
              f"token={access_token[:12]}…  expires_in={token_data['expires_in']}s")

    # ─── Bước 5: Gọi Resource API ─────────────
    _log_step(5, "GET /api/userinfo với Authorization: Bearer <token>",
              "Resource Server xác thực token, trả thông tin user")

    req2 = urllib.request.Request(
        "http://localhost:5000/api/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    with urllib.request.urlopen(req2) as r:
        user_info = json.loads(r.read())

    session["user_info"] = user_info
    _log_step(5, "Nhận user_info thành công ✓",
              f"email={user_info['email']}  name={user_info['name']}")

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# AUTHORIZATION SERVER  (giả lập)

# Bước 2: Hiển thị trang login/consent
@app.route("/oauth/authorize", methods=["GET", "POST"])
def oauth_authorize():
    """BƯỚC 2 — Auth Server hiển thị form đăng nhập & consent."""
    if request.method == "GET":
        client_id    = request.args.get("client_id")
        redirect_uri = request.args.get("redirect_uri")
        scope        = request.args.get("scope", "")
        state        = request.args.get("state")
        response_type = request.args.get("response_type")

        client = REGISTERED_CLIENTS.get(client_id)
        if not client:
            abort(400, "client_id không hợp lệ")
        if redirect_uri not in client["redirect_uris"]:
            abort(400, "redirect_uri không được phép")
        if response_type != "code":
            abort(400, "Chỉ hỗ trợ response_type=code")

        _log_step(2, "Auth Server hiện form login + consent",
                  f"client={client['name']}  scope={scope}")

        return render_template("authorize.html",
                               client=client, scope=scope.split(),
                               state=state, redirect_uri=redirect_uri,
                               client_id=client_id)

    # POST — user đã đăng nhập & bấm Cho phép
    username  = request.form.get("username", "").strip()
    password  = request.form.get("password", "")
    action    = request.form.get("action")
    state     = request.form.get("state")
    redirect_uri = request.form.get("redirect_uri")
    client_id    = request.form.get("client_id")
    scope        = request.form.get("scope", "")

    if action == "deny":
        return redirect(redirect_uri + "?" + urlencode({"error": "access_denied", "state": state}))

    user = USERS.get(username)
    if not user or user["password"] != password:
        _log_step(2, "Đăng nhập thất bại — sai username/password", "")
        return render_template("authorize.html",
                               client=REGISTERED_CLIENTS[client_id],
                               scope=scope.split(), state=state,
                               redirect_uri=redirect_uri, client_id=client_id,
                               error="Sai tên đăng nhập hoặc mật khẩu")

    # Sinh Authorization Code (dùng 1 lần, hết hạn sau 60s)
    code = gen_token(20)
    AUTH_CODES[code] = {
        "client_id":    client_id,
        "redirect_uri": redirect_uri,
        "user":         username,
        "scopes":       scope.split(),
        "expires":      time.time() + 60,
    }

    _log_step(2, "Xác thực thành công — sinh Authorization Code",
              f"user={username}  code={code[:8]}…")

    return redirect(redirect_uri + "?" + urlencode({"code": code, "state": state}))


# Bước 4: Token endpoint
@app.route("/oauth/token", methods=["POST"])
def oauth_token():
    """BƯỚC 4 — Đổi Authorization Code lấy Access Token."""
    grant_type    = request.form.get("grant_type")
    code          = request.form.get("code")
    redirect_uri  = request.form.get("redirect_uri")
    client_id     = request.form.get("client_id")
    client_secret = request.form.get("client_secret")

    if grant_type != "authorization_code":
        return jsonify(error="unsupported_grant_type"), 400

    client = REGISTERED_CLIENTS.get(client_id)
    if not client or client["client_secret"] != client_secret:
        return jsonify(error="invalid_client"), 401

    code_data = AUTH_CODES.pop(code, None)   # code chỉ dùng 1 lần
    if not code_data:
        return jsonify(error="invalid_grant", desc="Code không tồn tại"), 400
    if time.time() > code_data["expires"]:
        return jsonify(error="invalid_grant", desc="Code đã hết hạn"), 400
    if code_data["client_id"] != client_id:
        return jsonify(error="invalid_grant", desc="client_id không khớp"), 400
    if code_data["redirect_uri"] != redirect_uri:
        return jsonify(error="invalid_grant", desc="redirect_uri không khớp"), 400

    access_token  = gen_token(32)
    refresh_token = gen_token(32)
    ACCESS_TOKENS[access_token] = {
        "client_id": client_id,
        "user":      code_data["user"],
        "scopes":    code_data["scopes"],
        "expires":   time.time() + 3600,
    }

    return jsonify(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=3600,
        scope=" ".join(code_data["scopes"]),
    )


# Bước 5: Resource API
@app.route("/api/userinfo")
def api_userinfo():
    """BƯỚC 5 — Resource Server trả thông tin user sau khi xác thực token."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify(error="missing_token"), 401

    token = auth_header.split(" ", 1)[1]
    token_data = ACCESS_TOKENS.get(token)

    if not token_data:
        return jsonify(error="invalid_token"), 401
    if time.time() > token_data["expires"]:
        ACCESS_TOKENS.pop(token, None)
        return jsonify(error="token_expired"), 401

    user = USERS[token_data["user"]]
    response = {"sub": token_data["user"]}
    if "profile" in token_data["scopes"]:
        response["name"] = user["name"]
    if "email" in token_data["scopes"]:
        response["email"] = user["email"]
    response["scopes_granted"] = token_data["scopes"]
    return jsonify(response)


# ─── Debug: xem raw stores ────────────────────
@app.route("/debug")
def debug():
    """Xem trạng thái internal (chỉ dùng khi dev)."""
    return jsonify(
        auth_codes={k: {**v, "expires": f"+{v['expires']-time.time():.0f}s"}
                    for k, v in AUTH_CODES.items()},
        access_tokens={k[:12]+"…": {**v, "expires": f"+{v['expires']-time.time():.0f}s"}
                       for k, v in ACCESS_TOKENS.items()},
    )


# ──────────────────────────────────────────────
# Utility: ghi log bước vào session
# ──────────────────────────────────────────────
def _log_step(step_no, title, detail):
    steps = session.get("steps", [])
    steps.append({"step": step_no, "title": title, "detail": detail,
                  "time": time.strftime("%H:%M:%S")})
    session["steps"] = steps
    session.modified = True


if __name__ == "__main__":
    print("\n OAuth 2.0 Demo đang chạy → http://localhost:5000\n"
          "   Tài khoản thử: alice / 1234   hoặc   bob / 5678\n")
    app.run(debug=True, port=5000)