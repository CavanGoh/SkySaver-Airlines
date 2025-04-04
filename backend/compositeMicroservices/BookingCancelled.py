from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

# import sys
# sys.append.path("../wrapperServices")
# from ..wrapperServices.invokes import invoke_http



app = Flask(__name__)
CORS(app)

booking_URL = "http://localhost:5001/booking"
flexSeat_URL = "http://localhost:5003/flexseat"
seat_URL="http://localhost:8080/seats/flight"
@app.route("/booking_cancelled", methods=['POST'])
def cancel_booking():
    details = request.get_json()
    booking_id = details.get('booking_id')
    
    response = requests.put(booking_URL + "/cancel/" + str(booking_id))
    
    if response.status_code == 200:
            return jsonify({
                "code": 200,
                "message": "Booking cancelled successfully",
                "data": response.json().get("data")
            }), 200
    else:
        return jsonify(response.json()), response.status_code
    
# def processCancelBooking(booking):
#     #  Invoke other microservices: seat service to update seat to available
#     invoke_http(seat_URL, method="POST", json=order_result)
#      return


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)