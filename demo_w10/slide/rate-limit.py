from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

def get_user_id():
    return request.headers.get("X-User-ID", get_remote_address())

# --- KHỞI TẠO LIMITER ---
# 1. IP-BASED: 'key_func=get_remote_address' nghĩa là mặc định nó sẽ đếm request dựa trên IP.
# 2. SERVER-BASED: 'default_limits' áp dụng luật chung cho TOÀN BỘ server (mọi endpoint).
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "20 per hour"], # Giới hạn Server-based
    storage_uri="memory://" 
)

@app.route("/")
def index():
    return jsonify({
        "message": "Trang chủ. Áp dụng luật Server-based (100/ngày, 20/giờ) và IP-based."
    })

# 3. ENDPOINT-BASED
@app.route("/login", methods=["POST"])
@limiter.limit("3 per minute") # Ghi đè luật mặc định, chỉ cho phép 3 request/phút tại đây
def login():
    return jsonify({
        "message": "Endpoint đăng nhập. Giới hạn 3 request/phút theo IP để chống Brute-force."
    })

# 4. USER-BASED
@app.route("/api/profile")
@limiter.limit("5 per minute", key_func=get_user_id)
def profile():
    user_id = request.headers.get("X-User-ID", "Khách")
    return jsonify({
        "message": f"Dữ liệu profile của {user_id}. Giới hạn 5 request/phút riêng cho user này."
    })

@app.route("/ping")
@limiter.exempt
def ping():
    return jsonify({"message": "Pong! Endpoint này không bị giới hạn rate limit."})


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(
        error="Rate limit exceeded",
        description=str(e.description)
    ), 429

if __name__ == "__main__":
    app.run(debug=True, port=5000)