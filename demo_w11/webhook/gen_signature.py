import hmac
import hashlib
import json

WEBHOOK_SECRET = "webhook_secret"
payload = {
    "id": "evt_01",
    "type": "payment.succeeded",
    "user_id": 123
}

# Chuyển payload thành bytes
payload_bytes = json.dumps(payload).encode()

# Tạo HMAC SHA256 signature
signature = hmac.new(
    WEBHOOK_SECRET.encode(),
    msg=payload_bytes,
    digestmod=hashlib.sha256
).hexdigest()

print("Payload:", json.dumps(payload))
print("Signature:", signature)