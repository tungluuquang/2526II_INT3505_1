from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)


def process_v1(data):
    amount = data.get('amount')
    print(f"Processing V1 Payment: Amount = {amount}")
    return jsonify({
        "message": f"Payment of {amount} processed successfully (v1)."
    }), 200

def process_v2(data):
    amount = data.get('amount')
    currency = data.get('currency')
    print(f"Processing V2 Payment: Amount = {amount}, Currency = {currency}")
    return jsonify({
        "transaction_id": str(uuid.uuid4()),
        "status": "SUCCESS",
        "message": "Payment processed (v2)",
        "data": {
            "amount": amount,
            "currency": currency
        }
    }), 200


@app.route('/api/payments', methods=['POST'])
def process_payment():

    api_version = request.headers.get('X-API-Version', '1')
    
    data = request.get_json() or {}
    
    if api_version == '2':
        return process_v2(data)
    elif api_version == '1':
        return process_v1(data)
    else:
        return jsonify({"error": f"API version {api_version} is not supported"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)