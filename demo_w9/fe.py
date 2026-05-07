from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

FEATURE_TOGGLES = {
    "enable_v2_payment_gateway": False
}

def process_logic_v1(amount):
    return {"message": f"V1 (OLD LOGIC): Processed {amount}"}

def process_logic_v2(amount, currency):
    return {
        "transaction_id": str(uuid.uuid4()),
        "message": "V2 (NEW LOGIC): Super secure processing",
        "details": f"{amount} {currency}"
    }

@app.route('/api/payments', methods=['POST'])
def process_payment_with_flag():
    data = request.get_json() or {}
    amount = data.get('amount')
    currency = data.get('currency', 'VND')

    if FEATURE_TOGGLES.get("enable_v2_payment_gateway") is True:
        print("Feature Flag ON -> Routing to V2")
        result = process_logic_v2(amount, currency)
    else:
        print("Feature Flag OFF -> Routing to V1")
        result = process_logic_v1(amount)

    return jsonify({
        "status": "SUCCESS",
        "data": result,
        "_debug": {
            "v2_enabled": FEATURE_TOGGLES.get("enable_v2_payment_gateway")
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)