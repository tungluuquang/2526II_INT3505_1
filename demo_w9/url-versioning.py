from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)


@app.route('/api/v1/payments', methods=['POST'])
def process_payment_v1():
    data = request.get_json() or {}
    amount = data.get('amount')
    
    print(f"Processing V1 Payment: Amount = {amount}")
    
    return jsonify({
        "message": f"Payment of {amount} processed successfully (v1)."
    }), 200


@app.route('/api/v2/payments', methods=['POST'])
def process_payment_v2():
    data = request.get_json() or {}
    amount = data.get('amount')
    currency = data.get('currency') # v2 yêu cầu thêm loại tiền tệ
    
    print(f"Processing V2 Payment: Amount = {amount}, Currency = {currency}")
    
    response_data = {
        "transaction_id": str(uuid.uuid4()),
        "status": "SUCCESS",
        "message": "Payment processed (v2)",
        "data": {
            "amount": amount,
            "currency": currency
        }
    }
    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)