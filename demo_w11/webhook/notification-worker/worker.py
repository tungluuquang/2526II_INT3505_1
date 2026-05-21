import pika, json, time, os
from pika.exceptions import AMQPConnectionError

RABBIT_URL = os.environ.get("RABBIT_URL")

