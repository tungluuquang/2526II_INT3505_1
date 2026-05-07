from flask import Flask, request, jsonify
from werkzeug.exceptions import UnsupportedMediaType
import uuid

app = Flask(__name__)

def process_v1(data):
    amount = data.get('amount')
    return jsonify({
        "message": f"Payment of {amount} processed successfully (v1)."
    }), 200

def process_v2(data):
    amount = data.get('amount')
    currency = data.get('currency', 'VND') # Mặc định VND nếu quên truyền
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

    api_version = request.args.get('version', '1')
    
    data = request.get_json() 
    
    if not data:
        return jsonify({"error": "Body không được để trống"}), 400
        
    # Điều phối logic
    if api_version == '2':
        return process_v2(data)
    elif api_version == '1':
        return process_v1(data)
    else:
        return jsonify({"error": f"API version {api_version} is not supported"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)