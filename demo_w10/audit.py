import logging
import json
from datetime import datetime
from flask import Flask, request, jsonify, g
import time

app = Flask(__name__)

# Tạo một custom logger chuyên dụng cho Audit
audit_logger = logging.getLogger('audit_logger')
audit_logger.setLevel(logging.INFO)

# Ghi log ra file
file_handler = logging.FileHandler('audit.log')
file_handler.setLevel(logging.INFO)

# Formatter đơn giản (vì chúng ta sẽ truyền chuỗi JSON trực tiếp)
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
audit_logger.addHandler(file_handler)

def log_audit_event(action, status, details=None, user_id="anonymous"):
    """Hàm hỗ trợ ghi log audit chuẩn định dạng JSON"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "user_id": user_id,
        "action": action,
        "status": status,
        "ip_address": request.remote_addr,
        "user_agent": request.headers.get('User-Agent'),
        "method": request.method,
        "path": request.path,
        "details": details or {}
    }
    audit_logger.info(json.dumps(log_data))


@app.before_request
def start_timer():
    # Lưu thời gian bắt đầu request
    g.start_time = time.time()
    
    # Giả lập lấy thông tin user từ token (trong thực tế lấy từ JWT/Session)
    g.user_id = request.headers.get('X-User-Id', 'anonymous')

@app.after_request
def log_request(response):
    # Tính toán thời gian xử lý
    process_time = time.time() - g.start_time
    
    # Tự động ghi log mọi HTTP request (System Audit)
    log_audit_event(
        action="http_request",
        status="success" if response.status_code < 400 else "error",
        user_id=g.user_id,
        details={
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2)
        }
    )
    return response

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Hệ thống đang hoạt động"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    
    if username == "admin":
        log_audit_event("user_login", "success", {"username": username}, user_id="admin")
        return jsonify({"message": "Đăng nhập thành công!"})
    else:
        log_audit_event("user_login", "failed", {"username": username, "reason": "Sai thông tin"}, user_id="anonymous")
        return jsonify({"error": "Đăng nhập thất bại"}), 401

@app.route('/settings', methods=['PUT'])
def update_settings():
    if g.user_id == "anonymous":
        return jsonify({"error": "Chưa xác thực"}), 401
        
    data = request.json or {}
    
    log_audit_event(
        action="update_settings",
        status="success",
        user_id=g.user_id,
        details={
            "old_values": {"theme": "light", "notifications": True},
            "new_values": data
        }
    )
    return jsonify({"message": "Đã cập nhật cài đặt"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)