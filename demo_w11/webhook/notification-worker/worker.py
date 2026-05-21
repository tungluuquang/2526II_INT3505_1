import os
import json
import time
import signal
import logging
import pika
from pika.exceptions import AMQPConnectionError

RABBIT_URL = os.getenv("RABBIT_URL")
QUEUE_NAME = "notifications"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("notification-worker")

def connect_rabbitmq(url: str, retries: int = 10, delay: int = 5):
    if not url:
        raise RuntimeError("RABBIT_URL is not set")

    for i in range(retries):
        try:
            params = pika.URLParameters(url)
            connection = pika.BlockingConnection(params)
            logger.info("Connected to RabbitMQ")
            return connection

        except AMQPConnectionError:
            logger.warning(f"RabbitMQ not ready... retry {i + 1}/{retries}")
            time.sleep(delay)

    raise RuntimeError("Could not connect to RabbitMQ")

class NotificationWorker:
    def __init__(self, connection):
        self.connection = connection
        self.channel = connection.channel()
        self.channel.queue_declare(queue=QUEUE_NAME, durable=True)

        self._stopping = False

    def handle_event(self, event: dict):
        logger.info(f"Received event: {event}")

        # giả lập xử lý business logic
        time.sleep(1)

        logger.info(f"Notification sent for event_id={event.get('id')}")

    def callback(self, ch, method, properties, body):
        try:
            event = json.loads(body)
            self.handle_event(event)

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except json.JSONDecodeError:
            logger.error("Invalid JSON message")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

        except Exception as e:
            logger.exception(f"Processing error: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def start(self):
        logger.info("Worker started. Waiting for messages...")

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=QUEUE_NAME,
            on_message_callback=self.callback
        )

        while not self._stopping:
            try:
                self.connection.process_data_events(time_limit=1)
            except Exception as e:
                logger.error(f"Connection error: {e}")
                break

    def stop(self):
        logger.info("Stopping worker...")
        self._stopping = True
        try:
            self.connection.close()
        except Exception:
            pass

worker = None


def shutdown_handler(signum, frame):
    global worker
    if worker:
        worker.stop()


signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    connection = connect_rabbitmq(RABBIT_URL)
    worker = NotificationWorker(connection)
    worker.start()