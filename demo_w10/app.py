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

# --- CẤU HÌNH OPENTELEMETRY ĐỂ XUẤT TRACE RA UI (JAEGER/SIGNOZ) ---
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# 0. THIẾT LẬP TRACER PROVIDER VÀ EXPORTER
# Định danh service trên giao diện UI
resource = Resource(attributes={
    SERVICE_NAME: "flask-production-api"
})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Gửi dữ liệu qua OTLP HTTP (Mặc định Jaeger nghe ở port 4318)
otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)

# Sử dụng BatchSpanProcessor để tối ưu hiệu năng (gửi gom cụm thay vì gửi lẻ tẻ)
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

# Khởi tạo Flask app ĐẦU TIÊN
app = Flask(__name__)

# Tự động ghi lại trace cho các request của Flask
FlaskInstrumentor().instrument_app(app)

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

@app.route('/api/data', methods=['GET'])
@limiter.exempt 
def get_data():
    trace_id = request.headers.get("X-Correlation-ID", "unknown")

    # Tạo một custom span để theo dõi chi tiết quá trình xử lý logic bên trong
    with tracer.start_as_current_span("get_data_logic") as span:
        span.set_attribute("client.ip", request.remote_addr)
        span.set_attribute("trace.manual_id", trace_id)

        logger.info("Processing GET /api/data", extra={
            "client_ip": request.remote_addr,
            "trace_id": trace_id
        })

        try:
            # Gọi service bên ngoài (được bọc bởi Circuit Breaker)
            result = call_unstable_external_service()

            # trace success
            span.set_attribute("external.status", "success")

            return jsonify({
                "status": "success",
                "result": result,
                "trace_id": trace_id
            }), 200

        except pybreaker.CircuitBreakerError:
            span.set_attribute("circuit_breaker", "OPEN")
            span.set_status(trace.status.Status(trace.status.StatusCode.ERROR))
            
            logger.error("Circuit breaker is OPEN. Fast failing request.")

            return jsonify({
                "error": "Service temporarily unavailable due to high failure rate.",
                "trace_id": trace_id
            }), 503

        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.status.Status(trace.status.StatusCode.ERROR))

            logger.error(f"Internal Error: {str(e)}", exc_info=True)

            return jsonify({
                "error": "Internal server error",
                "trace_id": trace_id
            }), 500

if __name__ == '__main__':
    # Lưu ý: Port 5000 cho Flask app
    app.run(host='0.0.0.0', port=5000)