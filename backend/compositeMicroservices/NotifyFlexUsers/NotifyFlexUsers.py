import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wrapperServices.invokes import invoke_http

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import pika

app = Flask(__name__)
CORS(app)

# Microservice URLs
flight_URL = "http://localhost:5000/flights"    
flexseat_URL = "http://localhost:5003/flexseat"

# RabbitMQ setup
RABBITMQ_HOST = "localhost"
RABBITMQ_PORT = 5672
EXCHANGE_NAME = "notification_direct"
ROUTING_KEY = "notification"

@app.route("/notify_flex_user", methods=["POST"])
def notify_flex_user():
    if request.is_json:
        try:
            data = request.get_json()
            print("\nReceived cancellation event:", data)

            cancelled_flight_id = data.get("flight_id")
            cancelled_date = data.get("date")  

            if not cancelled_flight_id or not cancelled_date:
                return jsonify({
                    "code": 400,
                    "message": "Missing required fields: flight_id or date"
                }), 400

            # Step 1: Get flight details
            print("\n----- Retrieving flight details -----")
            try:
                flight_result = invoke_http(f"{flight_URL}/{cancelled_flight_id}", method="GET")
                print("Flight result:", flight_result)
            except Exception as e:
                return jsonify({
                    "code": 500,
                    "message": f"Invalid response from flight service: {str(e)}"
                }), 500

            if not isinstance(flight_result, dict) or flight_result.get("code") != 200:
                return jsonify({
                    "code": 404,
                    "message": "Flight not found or error retrieving flight data",
                    "data": flight_result
                }), 404

            flight_data = flight_result["data"]

            # Step 2: Query flex users with matching destination and departureDate
            print("\n----- Retrieving matching flex users -----")
            query = {
                "destination": flight_data["destination"],
                "departureDate": cancelled_date  # Matches field name from flight DB
            }

            try:
                flex_result = invoke_http(flexseat_URL, method="POST", json=query)
                print("Flex user match result:", flex_result)
            except Exception as e:
                return jsonify({
                    "code": 500,
                    "message": f"Invalid response from flexseat service: {str(e)}"
                }), 500

            if not isinstance(flex_result, dict) or flex_result.get("code") != 200 or not flex_result.get("data"):
                return jsonify({
                    "code": 200,
                    "message": "No matching flex users found for this cancellation.",
                    "data": []
                }), 200

            matched_users = flex_result["data"]

            # Step 3: Publish notifications to RabbitMQ
            print("\n----- Sending notifications via RabbitMQ -----")
            publish_to_queue({
                "type": "flight_cancellation",
                "flight": flight_data,
                "date": cancelled_date,
                "users": matched_users
            })

            return jsonify({
                "code": 200,
                "message": f"Notified {len(matched_users)} flex user(s)",
                "data": matched_users
            }), 200

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            err_msg = f"{str(e)} at {exc_type}: {fname}: line {exc_tb.tb_lineno}"
            print("Error:", err_msg)

            return jsonify({
                "code": 500,
                "message": "Internal server error: " + err_msg
            }), 500

    return jsonify({
        "code": 400,
        "message": "Request must be in JSON format"
    }), 400


def publish_to_queue(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        heartbeat=300,
        blocked_connection_timeout=300
    ))

    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct", durable=True)

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=ROUTING_KEY,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # Make message persistent
    )

    print("Published message to RabbitMQ.")
    connection.close()


if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for notifying flex users...")
    app.run(host="0.0.0.0", port=5200, debug=True)



