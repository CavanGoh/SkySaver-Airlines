import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wrapperServices.invokes import invoke_http

import json
import pika
import requests

flight_url = "http://localhost:5000"
flexseat_url = "http://localhost:5003"
notification_url = "http://localhost:5021"

# RabbitMQ setup
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
EXCHANGE_NAME = "notify_direct"
ROUTING_KEY = "notify"

def notify_flex_user(data):
    try:
        print(data)
        flight_id = data.get("flight")
        seat_id = data.get("seat")
        
        #access flight 
        get_flight_details = requests.get(flight_url + f"/flight/{flight_id}")
        if get_flight_details.status_code == 200:
            flight_details = get_flight_details.json()
            departure = flight_details.get("data", {}).get("departure")
            destination = flight_details.get("data", {}).get("destination") 
            departureDate = flight_details.get("data", {}).get("departureDate")
            
        #get flex user
        flex_response = requests.get(
            flexseat_url + "/flexseat/match", 
            params={
                "departure": departure,
                "destination": destination,
                "departureDate": departureDate
            }
        )
        if flex_response.status_code == 200:
            flex_data = flex_response.json().get("data", {})
            flex_users = flex_data.get("users", [])
            print("FlexSeat match data:", flex_data)
    
            if flex_users:
                for user in flex_users:
                    # Send notifications to matching users
                    notification_data = {
                        "users": [user["userId"]],
                        "flex_id": user["flexId"],
                        "flight_details": {
                            "id": flight_id,
                            "departure": departure,
                            "destination": destination,
                            "departureDate": departureDate
                        },
                        "seat_id": seat_id
                    }
                    
                    # Call notification service
                    notification_response = requests.post(
                        notification_url + "/send-notifications",
                        json=notification_data
                    )
                    
                    print(f"Notification sent: {notification_response.status_code}")
                    print(f"Response: {notification_response.json()}")
            
    except Exception as e:
        print(f"Error in notify_flex_user: {str(e)}")
        
def callback(ch, method, properties, body):
    try:
        data = json.loads(body.decode())
        notify_flex_user(data)
    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.basic_consume(queue='notify', on_message_callback=callback)

    print("Listening for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()



