from flask import Flask, request, jsonify
import random

app = Flask(__name__)

metrics_db = {
    "v1": {"total_requests": 0, "error_count": 0, "unique_clients": set()},
    "v2": {"total_requests": 0, "error_count": 0, "unique_clients": set()}
}

@app.route('/api/v1/payments', methods=['POST'])
def payment_v1():
    client_id = request.headers.get('X-Client-ID', 'unknown_client')

    metrics_db["v1"]["total_requests"] += 1
    metrics_db["v1"]["unique_clients"].add(client_id)

    if random.random() < 0.2:
        metrics_db["v1"]["error_count"] += 1
        return jsonify({"error": "Lỗi hệ thống cũ"}), 500

    return jsonify({"message": "Thanh toán V1 thành công"}), 200


@app.route('/api/v2/payments', methods=['POST'])
def payment_v2():
    client_id = request.headers.get('X-Client-ID', 'unknown_client')

    metrics_db["v2"]["total_requests"] += 1
    metrics_db["v2"]["unique_clients"].add(client_id)

    if random.random() < 0.05:
        metrics_db["v2"]["error_count"] += 1
        return jsonify({"error": "Lỗi hệ thống mới"}), 500

    return jsonify({"message": "Thanh toán V2 thành công, siêu tốc"}), 200

@app.route('/admin/metrics', methods=['GET'])
def get_migration_metrics():
    req_v1 = metrics_db["v1"]["total_requests"]
    req_v2 = metrics_db["v2"]["total_requests"]
    total_reqs = req_v1 + req_v2

    adoption_rate = 0
    if total_reqs > 0:
        adoption_rate = round((req_v2 / total_reqs) * 100, 2)

    error_rate_v1 = 0
    if req_v1 > 0:
        error_rate_v1 = round((metrics_db["v1"]["error_count"] / req_v1) * 100, 2)

    error_rate_v2 = 0
    if req_v2 > 0:
        error_rate_v2 = round((metrics_db["v2"]["error_count"] / req_v2) * 100, 2)

    clients_v1 = metrics_db["v1"]["unique_clients"]
    clients_v2 = metrics_db["v2"]["unique_clients"]

    total_unique_clients = len(clients_v1.union(clients_v2))

    migration_progress = 0
    if total_unique_clients > 0:
        migration_progress = round((len(clients_v2) / total_unique_clients) * 100, 2)

    return jsonify({
        "1. Adoption_Rate": f"{adoption_rate}% request đang trỏ vào V2",
        "2. Error_Rate_Comparison": {
            "v1_error_rate": f"{error_rate_v1}%",
            "v2_error_rate": f"{error_rate_v2}%"
        },
        "3. Migration_Progress": f"{migration_progress}% client đã dùng V2 ({len(clients_v2)}/{total_unique_clients} clients)",
        "Raw_Data": {
            "v1": {
                "requests": req_v1,
                "errors": metrics_db["v1"]["error_count"],
                "active_clients": list(clients_v1)
            },
            "v2": {
                "requests": req_v2,
                "errors": metrics_db["v2"]["error_count"],
                "active_clients": list(clients_v2)
            }
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)