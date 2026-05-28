from flask import Flask, request, jsonify, abort
import pika
import json
import os
import hmac
import hashlib
import time

class Config:
    RABBIT_URL = os.getenv("RABBIT_URL")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
    QUEUE_NAME = "notifications"

    @staticmethod
    def validate():
        if not Config.RABBIT_URL:
            raise RuntimeError("RABBIT_URL is not set")
        if not Config.WEBHOOK_SECRET:
            raise RuntimeError("WEBHOOK_SECRET is not set")


Config.validate()


def verify_signature(secret: str, payload: bytes, signature: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature or "")

class RabbitMQClient:
    def __init__(self, url: str):
        self.params = pika.URLParameters(url)
        self.params.heartbeat = 600
        self.params.blocked_connection_timeout = 300

        self.connection = None
        self.channel = None

        self.connect()

    def connect(self):
        for i in range(10):
            try:
                self.connection = pika.BlockingConnection(self.params)
                self.channel = self.connection.channel()

                self.channel.queue_declare(
                    queue=Config.QUEUE_NAME,
                    durable=True
                )

                print("RabbitMQ connected")
                return

            except Exception as e:
                print(f"[RabbitMQ] retry {i+1}/10 failed: {e}")
                time.sleep(3)

        raise Exception("Cannot connect to RabbitMQ")

    def publish(self, message: dict):
        if not self.channel:
            self.connect()

        self.channel.basic_publish(
            exchange="",
            routing_key=Config.QUEUE_NAME,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

rabbit_client = None

def get_rabbit():
    global rabbit_client
    if rabbit_client is None:
        rabbit_client = RabbitMQClient(Config.RABBIT_URL)
    return rabbit_client


# Flask App
app = Flask(__name__)


@app.route("/webhooks/events", methods=["POST"])
def handle_webhook():
    payload_body = request.data
    signature = request.headers.get("X-Signature")

    if not verify_signature(Config.WEBHOOK_SECRET, payload_body, signature):
        abort(401, description="Invalid signature")

    try:
        payload = json.loads(payload_body)
    except json.JSONDecodeError:
        abort(400, description="Invalid JSON payload")

    get_rabbit().publish(payload)

    return jsonify({"status": "queued"}), 200


@app.route("/")
def health():
    return jsonify({"status": "ok"}), 200


# Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)