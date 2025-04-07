from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import pika
import json
from datetime import datetime

app = Flask(__name__)
# CORS(app)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])



booking_URL = "http://booking:5001/booking"
seat_URL="http://seat:8080/seats"

amqp_host = "localhost"
amqp_port = 5672
exchange_name = "notify_direct"
exchange_type = "direct"
routing_key = "notify"

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
        
        # Declare the exchange
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
    flight_id = details.get('flight_id')
    seat_id = details.get('seat_id')
    
    booking_response = requests.put(booking_URL + "/cancel/" + str(booking_id))
    if booking_response.status_code == 200:
        seat_response = requests.put(
        f"{seat_URL}/{flight_id}/{seat_id}/availability",
        json={"availability": True}
)
        if seat_response.status_code == 200:
            print("Seat updated", seat_response.status_code)
            
            message = {
                "event_type": "booking_cancelled",
                "flight": flight_id,
                "seat": seat_id,
                "timestamp": datetime.now().isoformat(),
                "details": {
                "message": f"Flight #{flight_id} has cancellation",
                "status": "cancelled"
                }
            }
            
            publish_result = publish_message(message)
        
            return jsonify({
                "code": 200,
                "message": "Booking cancelled successfully",
                "data": booking_response.json().get("data"),
                "notification_sent": publish_result
            }), 200
        else:
            # Add a return for seat service failure
            return jsonify({
                "code": seat_response.status_code,
                "message": "Failed to update seat availability"
            }), 500
            
    return jsonify({
        "code": booking_response.status_code,
        "message": "Failed to cancel booking"
    }), booking_response.status_code

    
# def processCancelBooking(booking):
#     #  Invoke other microservices: seat service to update seat to available
#     invoke_http(seat_URL, method="POST", json=order_result)
#      return


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)