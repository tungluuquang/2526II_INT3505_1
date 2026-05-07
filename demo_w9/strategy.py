from flask import Flask, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

@app.route('/api/v1/payments', methods=['POST'])
def process_payment_deprecated():
    data = request.get_json() or {}
    amount = data.get('amount')

    print(f"Processing OLD Payment: Amount = {amount}")

    response_body = {
        "status": "SUCCESS",
        "message": f"Payment of {amount} processed.",
        "_meta": {
            "is_deprecated": True,
            "sunset_date": "2026-12-31T23:59:59Z",
            "warning": "Endpoint này sẽ bị ngừng hoạt động vào cuối năm 2026. Vui lòng chuyển sang dùng /api/v2/payments",
            "docs_url": "https://yourdomain.com/docs/api/v2/payments"
        }
    }

    response = jsonify(response_body)
    response.status_code = 200

    response.headers['Deprecation'] = 'true'
    response.headers['Sunset'] = 'Thu, 31 Dec 2026 23:59:59 GMT'
    response.headers['Link'] = '<https://yourdomain.com/docs/api/v2/payments>; rel="deprecation"; type="text/html"'

    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)