from flask import Flask, request, jsonify
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)

booking_URL = "http://localhost:5000/booking"

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5100, debug=True)