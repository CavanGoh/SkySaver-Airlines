import pika
import json
import requests

# RabbitMQ Connection Settings
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "notifications.queue"
OUTSYSTEMS_API_URL = "https://your-outsystems-app.com/api/notifications"

def callback(ch, method, properties, body):
    notification = json.loads(body)
    print(f" [x] Received notification: {notification}")

    # Send notification to OutSystems API
    response = requests.post(OUTSYSTEMS_API_URL, json=notification)

    if response.status_code == 200:
        print(" [✓] Notification sent to OutSystems successfully.")
    else:
        print(" [X] Failed to send notification to OutSystems.")

# Setup RabbitMQ Connection
def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    # Declare queue
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Consume messages
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)

    print(" [*] Waiting for notifications. To exit, press CTRL+C")
    channel.start_consuming()

# Run the consumer
if __name__ == "__main__":
    start_consumer()
