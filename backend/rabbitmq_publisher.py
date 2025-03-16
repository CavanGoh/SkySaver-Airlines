import pika
import json

# RabbitMQ Connection Settings
RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "notifications.exchange"

def publish_notification(user_id, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_HOST))
    channel = connection.channel()

    # Declare exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout")

    # Create notification message
    notification = {
        "user_id": user_id,
        "message": message
    }

    # Publish message to exchange
    channel.basic_publish(exchange=EXCHANGE_NAME, routing_key="", body=json.dumps(notification))

    print(f" [x] Sent notification: {notification}")
    connection.close()

# Example usage
if __name__ == "__main__":
    publish_notification("12345", "Your Smart Flex Booking is confirmed.")
