import requests, hmac, hashlib, json

WEBHOOK_SECRET = "webhook_secret"
payload = {
    "id": "evt_01",
    "type": "payment.succeeded",
    "user_id": 123
}
payload_bytes = json.dumps(payload, separators=(',', ':')).encode()  # loại bỏ space
signature = hmac.new(WEBHOOK_SECRET.encode(), payload_bytes, hashlib.sha256).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature": signature
}

resp = requests.post("http://localhost:5000/webhooks/events", headers=headers, data=payload_bytes)
print(resp.status_code, resp.text)