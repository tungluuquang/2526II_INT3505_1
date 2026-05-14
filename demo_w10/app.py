import os
import logging
import time
import random
from flask import Flask, jsonify, request
from pythonjsonlogger import jsonlogger
from prometheus_flask_exporter import PrometheusMetrics
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pybreaker
from werkzeug.middleware.proxy_fix import ProxyFix

# Khởi tạo Flask app ĐẦU TIÊN
app = Flask(__name__)

# BÁO CHO FLASK BIẾT NÓ ĐANG ĐỨNG SAU PROXY (Cloudflare/Render) ĐỂ LẤY IP THẬT
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# 1. THIẾT LẬP LOGGING
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
logHandler.setFormatter(formatter)

# Tạo logger riêng cho API
logger = logging.getLogger('my_api') 
logger.setLevel(logging.INFO)
logger.addHandler(logHandler)

# Tắt log nhiễu mặc định của Flask/Werkzeug
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)

# 2. THIẾT LẬP METRICS (Prometheus)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Flask API Production', version='1.0.0')

# 3. THIẾT LẬP RATE LIMITING
REDIS_URL = os.getenv("REDIS_URL", "memory://")

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1000 per day", "100 per hour"],
    storage_uri=REDIS_URL
)
 
# 4. THIẾT LẬP CIRCUIT BREAKER
class CircuitBreakerLogger(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        msg = f"Circuit Breaker state changed from {old_state.name} to {new_state.name}"
        if new_state == pybreaker.STATE_OPEN:
            logger.error(msg, extra={"alert": "CRITICAL_EXTERNAL_SERVICE_DOWN"})
        elif new_state == pybreaker.STATE_HALF_OPEN:
            logger.warning(msg, extra={"alert": "TESTING_EXTERNAL_SERVICE"})
        else:
            logger.info(msg, extra={"alert": "EXTERNAL_SERVICE_RECOVERED"})

external_api_breaker = pybreaker.CircuitBreaker(
    fail_max=3, 
    reset_timeout=15,
    listeners=[CircuitBreakerLogger()] 
)

@external_api_breaker
def call_unstable_external_service():
    """Giả lập việc gọi một API bên ngoài hoặc Database bị chập chờn"""
    if random.choice([True, False]):
        raise Exception("External service timeout or 500 Error!")
    time.sleep(0.5) 
    return {"data": "Data from external service"}

# 5. ĐỊNH NGHĨA CÁC ENDPOINT (ROUTES)
@app.route('/api/health')
@limiter.exempt 
def health_check():
    return jsonify({"status": "healthy"}), 200

# API MỚI: DEMO RATE LIMIT
@app.route('/api/test-limit', methods=['GET'])
@limiter.limit("5 per minute")
def test_limit():
    logger.info("Processing GET /api/test-limit - Test Rate Limiting", extra={
        "client_ip": request.remote_addr
    })
    return jsonify({"message": "API is stable, just for Rate Limit tests"}), 200

# API CŨ: CHUYÊN ĐỂ DEMO CIRCUIT BREAKER (Tắt Rate limit đi để dễ F5)
@app.route('/api/data', methods=['GET'])
@limiter.exempt # Tắt Rate Limit ở đây để F5 thoải mái không bị dính 429
def get_data():
    trace_id = request.headers.get("X-Correlation-ID", "unknown")
    
    logger.info("Processing GET /api/data", extra={
        "client_ip": request.remote_addr,
        "trace_id": trace_id
    })

    try:
        result = call_unstable_external_service()
        return jsonify({"status": "success", "result": result}), 200
        
    except pybreaker.CircuitBreakerError:
        logger.error("Circuit breaker is OPEN. Fast failing request.")
        return jsonify({
            "error": "Service temporarily unavailable due to high failure rate. Please try again later."
        }), 503
        
    except Exception as e:
        logger.error(f"Internal Error: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)