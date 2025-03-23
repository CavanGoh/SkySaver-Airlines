import pika 
import json

def publish_booking(user_id, status):
    #connect to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
        ))
    channel = connection.channel()
    
    #declare the exchange 
    channel.exchange_declare(exchange='flight_booking_exchange', exchange_type='topic')
    
    #create the message payload
    message = {
        "event": "booking_confirmed",
        "data": {
            "user_id": user_id,
            "status": status
        }        
    }
    
    #publish the message with a routing key 
    channel.basic_publish(
        exchange='flight_booking_exchange',
        routing_key = 'booking.confirmed',
        body=json.dumps(message)
    )
    
    print(f"Published booking confirmed event: {message}")
    connection.close()
    
if __name__ == "__main__":
    publish_booking("12345", "confirmed")