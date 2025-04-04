import pika
import json
import time


# Configuration
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
EXCHANGE_NAME = "notification_direct"
EXCHANGE_TYPE = "direct"
QUEUE_NAME = "notification"
ROUTING_KEY = "notification"

def consume_messages():

    while True:
        try:
            # Connect to RabbitMQ
            print(f"Connecting to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}...")
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT,
                    heartbeat=300,
                    blocked_connection_timeout=300
                )
            )
            channel = connection.channel()
            
            # Declare exchange and queue (ensuring they exist)
            channel.exchange_declare(
                exchange=EXCHANGE_NAME,
                exchange_type=EXCHANGE_TYPE,
                durable=True
            )
            
            # Declare and bind the queue
            channel.queue_declare(queue=QUEUE_NAME, durable=True)
            channel.queue_bind(
                exchange=EXCHANGE_NAME,
                queue=QUEUE_NAME,
                routing_key=ROUTING_KEY
            )
            
            print(f"Connected to RabbitMQ, waiting for messages on queue: {QUEUE_NAME}")
            
            # Define the message handler
            def callback(ch, method, properties, body):
                try:
                    # Parse the message
                    message = json.loads(body)
                    print("\n---------- NOTIFICATION RECEIVED ----------")
                    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"Message: {json.dumps(message, indent=2)}")
                    print("------------------------------------------\n")
                    
                    # Acknowledge the message
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    
                except Exception as e:
                    print(f"Error processing message: {str(e)}")
                    # Negative acknowledgment - requeue the message
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            
            # Set up the consumer with prefetch count of 1
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue=QUEUE_NAME,
                on_message_callback=callback
            )
            
            print("Ready to receive messages.")
            channel.start_consuming()
            
        except KeyboardInterrupt:
            print("Interrupted by user. Shutting down...")
            break
        except Exception as e:
            print(f"RabbitMQ connection error: {str(e)}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)

if __name__ == '__main__':
    print("Starting notification consumer...")
    consume_messages()