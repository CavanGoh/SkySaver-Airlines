from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pika
import json
from datetime import datetime

app = Flask(__name__)
# CORS(app)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])


# URLs for microservices
# booking_URL = "http://localhost:5000/booking"
# flexSeat_URL = "http://localhost:5001/flexseat"

booking_URL = "http://localhost:5001/booking"
flexSeat_URL = "http://localhost:5003/flexseat"
seat_URL="http://localhost:8080/seats/flight"

amqp_host = "localhost"
amqp_port = 5672
exchange_name = "notification_direct"
exchange_type = "direct"
routing_key = "notification"

def publish_message(message):

    try:

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=amqp_host,
                port=amqp_port,
                heartbeat=300,
                blocked_connection_timeout=300,
            )
        )
        

        channel = connection.channel()
        
        channel.exchange_declare(
            exchange=exchange_name, 
            exchange_type=exchange_type, 
            durable=True
        )
        
        # Publish the message
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
                content_type='application/json'
            )
        )
        
        print(f"Published message to RabbitMQ: {message}")
        

        connection.close()
        return True
        
    except Exception as e:
        print(f"Error publishing message to RabbitMQ: {str(e)}")
        return False



@app.route("/booking_cancelled", methods=['POST'])
def cancel_booking():
    details = request.get_json()
    booking_id = details.get('booking_id')
    
    response = requests.put(booking_URL + "/cancel/" + str(booking_id))
    
    if response.status_code == 200:
        #hardcode until flight is ready
        departure = "New York"
        destination = "London"
        departureDate = "2025-04-15"
        flex_url = f"{flexSeat_URL}/match"
        print(f"Calling FlexSeat API at: {flex_url}")
            
            # Make request to FlexSeat service
        flex_response = requests.get(
            flex_url, 
            params={
                "departure": departure,
                "destination": destination,
                "departureDate": departureDate
            }
        )
        if flex_response.status_code == 200:
            flex_data = flex_response.json().get("data", {})
            print("FlexSeat match data:", flex_data)
        
        notification_message = {
            "event_type": "booking_cancelled",
            "booking_id": booking_id,
            "timestamp": datetime.now().isoformat(),
            "details": {
            "message": f"Booking #{booking_id} has been cancelled",
            "status": "cancelled"
            }
        }
            

        publish_result = publish_message(notification_message)
        

        return jsonify({
            "code": 200,
            "message": "Booking cancelled successfully",
            "data": response.json().get("data"),
            "notification_sent": publish_result
        }), 200
    else:
        return jsonify(response.json()), response.status_code
    
# def processCancelBooking(booking):
#     #  Invoke other microservices: seat service to update seat to available
#     invoke_http(seat_URL, method="POST", json=order_result)
#      return


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)