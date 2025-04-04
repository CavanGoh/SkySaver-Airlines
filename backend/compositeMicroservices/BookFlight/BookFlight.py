from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wrapperServices.invokes import invoke_http


app = Flask(__name__)
# CORS(app)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])


booking_URL = "http://localhost:5001/booking/new"
seat_URL="http://localhost:8080/seats"
@app.route("/book_flight", methods=['POST'])
def book_flight():
    if request.is_json:
        try:
            details=request.get_json()
            user_id=details["user_id"]
            flight_id=details["flight_id"]
            seat=details["seat_id"]
            print("\nReceived a booking in JSON:", details)
            
            # Create a new dictionary with only the relevant details
            #To decrease Payload Size: reduce size of the request and response payloads
            # reduce Security and Privacy Risks
            # booking_details = {
            #     "user_id": user_id,
            #     "flight_id": flight_id
            # }
            # seat_details = {
            #     "flight_id": flight_id,
            #     "seatID": seat
            # }
            print('\n-----Invoking Booking microservice-----')
            booking_result=invoke_http(booking_URL, method='POST', json=details)
            
            if booking_result["code"] in range(200,300):
                    print('\n-----Booking microservice creation G-----')
                    print('\n-----Now Invoking seat microservice-----')
                    update_availability_url=seat_URL+"/"+str(flight_id)+"/"+seat+"/availability"
                    seat_change=invoke_http(update_availability_url, method='PUT', json={"availability":False})


                    if seat_change["code"] in range(200,300):
                        return jsonify({
                            "code": 200,
                            "message": "Booking created+seat avail updated successfully",
                            # "data": booking_result.json().get("data")
                        }), 200
                    else:
                         return jsonify({
                            "code": 500,
                            "message": "Seat Update failure",
                            # "data": booking_result.json().get("data")
                        })
            else:
                return {
                     "code": booking_result["code"],
                     "data": {"booking_result":booking_result},
                     "message": "Booking creation failure."
                }
            
        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "BookFlight.py internal error: " + ex_str
            }), 500
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)