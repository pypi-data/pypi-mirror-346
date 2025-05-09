import pika
import json
import signal
import time
import traceback
from pika.exceptions import AMQPConnectionError, ChannelWrongStateError
from cneura_ai.logger import logger


class MessageWorker:
    def __init__(self, input_queue: str, output_queue: str, process_message, host: str = 'localhost', username: str = None, password: str = None, dlq: str = None):
        self.host = host
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.process_message = process_message
        self.dlq = dlq
        self.connection = None
        self.channel = None
        self.credentials = pika.PlainCredentials(username, password) if username and password else None
        self.parameters = pika.ConnectionParameters(
            host=self.host,
            credentials=self.credentials,
            heartbeat=60,
            blocked_connection_timeout=30
        ) if self.credentials else pika.ConnectionParameters(
            host=self.host,
            heartbeat=60,
            blocked_connection_timeout=30
        )

        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def reconnect(self, consume: bool = False):
        """Reconnect to RabbitMQ if connection fails."""
        while True:
            try:
                self.connection = pika.BlockingConnection(self.parameters)
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.input_queue, durable=True)
                self.channel.queue_declare(queue=self.output_queue, durable=True)
                if self.dlq:
                    self.channel.queue_declare(queue=self.dlq, durable=True)
                self.channel.basic_qos(prefetch_count=1)
                if consume:
                    self.channel.basic_consume(queue=self.input_queue, on_message_callback=self.callback, auto_ack=False)
                logger.info("[*] Connected to RabbitMQ")
                break
            except AMQPConnectionError as e:
                logger.error(f"[!] Connection failed: {e}, retrying in 5 seconds...")
                time.sleep(5)

    def callback(self, ch, method, properties, body):
        try:
            message = json.loads(body)
            response = self.process_message(message)
            logger.debug(f"[>] process_message response: {response}")

            if not isinstance(response, dict):
                raise ValueError("process_message must return a dictionary")

            if "data" not in response:
                raise ValueError("Missing 'data' in process_message response")

            response_data = response["data"]
            target_queue = response.get("queue") or self.output_queue

            response_json = json.dumps(response_data)
            self.ensure_queue(target_queue)
            self.safe_publish(target_queue, response_json)
            logger.info(f"[x] Sent to '{target_queue}': {response_json}")

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception:
            logger.exception("[!] Error processing message")
            if self.dlq:
                try:
                    headers = properties.headers if properties and properties.headers else {}
                    retries = headers.get('x-retries', 0)
                    if retries >= 3:
                        logger.error(f"[!] Max retries reached for message: {body}")
                    else:
                        headers['x-retries'] = retries + 1
                        self.safe_publish(self.dlq, body, headers=headers)
                        logger.warning(f"[!] Message sent to DLQ '{self.dlq}' with retry count: {headers['x-retries']}")
                except Exception as e:
                    logger.exception(f"[!] Failed to publish to DLQ: {e}")
            ch.basic_ack(delivery_tag=method.delivery_tag)


    def ensure_queue(self, queue_name):
        """Declare the queue if it does not exist to prevent errors."""
        try:
            self.channel.queue_declare(queue=queue_name, durable=True)
        except Exception as e:
            logger.error(f"[!] Failed to declare queue '{queue_name}': {e}")

    def safe_publish(self, queue, message, headers=None):
        """Ensure message is published even after connection loss."""
        while True:
            try:
                if not self.channel or self.channel.is_closed:
                    logger.warning("[!] Channel is closed, reconnecting before publishing...")
                    self.reconnect()
                props = pika.BasicProperties(headers=headers) if headers else None
                self.channel.basic_publish(exchange='', routing_key=queue, body=message, properties=props)
                return
            except (AMQPConnectionError, ChannelWrongStateError):
                logger.error("[!] Connection/channel issue during publish, reconnecting...")
                self.reconnect()

    def start(self):
        """Start consuming messages from input queue."""
        logger.info(f"[*] Listening for messages in '{self.input_queue}'...")
        self.reconnect(consume=True)
        while True:
            try:
                self.channel.start_consuming()
            except (AMQPConnectionError, ChannelWrongStateError) as e:
                logger.error(f"[!] Connection/channel error: {e}, reconnecting...")
                self.reconnect(consume=True)
            except Exception:
                logger.exception("[!] Unexpected error, stopping worker...")
                self.stop()
                break

    def stop(self):
        """Stop consuming messages and close connection."""
        if self.channel and self.channel.is_open:
            self.channel.stop_consuming()
        if self.connection and self.connection.is_open:
            self.connection.close()
        logger.info("[!] Worker stopped.")

    def handle_shutdown(self, signum, frame):
        """Handle shutdown signals (SIGINT, SIGTERM)."""
        logger.info("[!] Received shutdown signal. Stopping worker...")
        self.stop()
