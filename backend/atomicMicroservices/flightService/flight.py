import os
import base64
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, jsonify, request
# from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
# CORS(app)
# CORS(app, supports_credentials=True, origins=["http://localhost:5173"])


# Load environment variables from .env file
load_dotenv()

# Load Firebase credentials securely from environment variable (Base64 encoded)
firebase_credentials_base64 = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_credentials_base64:
    raise Exception("Firebase credentials not found in environment variables")

# Decode the Base64 string back to JSON
firebase_json = base64.b64decode(firebase_credentials_base64).decode("utf-8")
cred_dict = json.loads(firebase_json)

# Initialize Firebase using the credentials
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://skysaver-db-default-rtdb.firebaseio.com/'
})

# Connect to RTDB
ref = db.reference("flights")  # Reference to the "flights" node in RTDB

# Function to convert date format from DD-MM-YYYY to YYYY-MM-DD
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%d-%m-%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        # Try another common format in case the input is already YYYY-MM-DD
        try:
            # Validate if it's already in YYYY-MM-DD format
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str  # Already in desired format
        except ValueError:
            return date_str  # Return original if conversion fails

# Get filtered flights BY departure, destination, and the flights taht fall between the 2 dates
@app.route("/flights", methods=['GET'])
def get_filtered_flights():
    try:
        # Get query parameters from the URL
        departure = request.args.get('departure')
        destination = request.args.get('destination')
        date_from = request.args.get('dateFrom')  # 'DD-MM-YYYY' format
        date_to = request.args.get('dateTo')    # 'DD-MM-YYYY' format

        # Parse the dateFrom and dateTo into datetime objects
        if date_from:
            date_from = datetime.strptime(date_from, "%d-%m-%Y")
        if date_to:
            date_to = datetime.strptime(date_to, "%d-%m-%Y")

        # Fetch all flights from Firebase (Note: This might not scale well with large datasets)
        flights = ref.get()

        # If no query parameters are provided, return all flights
        if not departure and not destination and not date_from and not date_to:
            if isinstance(flights, list):
                for flight in flights:
                    flight['departureDate'] = format_date(flight['departureDate'])
            return jsonify({"code": 200, "data": {"flights": flights}})

        # Manually filter by the provided query parameters
        filtered_flights = []

        # Ensure flights is an iterable object (check if it's a dictionary or list)
        if isinstance(flights, dict):
            flights = list(flights.values())  # Convert dict to list if necessary

        for flight in flights:
            # Apply filters
            if flight.get('departure') != departure:
                continue
            if flight.get('destination') != destination:
                continue

            # Apply date range filters (ensure both dates are parsed correctly)
            
            flight_date = datetime.strptime(flight['departureDate'], "%d-%m-%Y")
            if flight_date < date_from or flight_date > date_to:
                continue


            # If flight matches all filters, add it to the results
            filtered_flights.append(flight)

        # Return filtered results or 404 if no matching flights are found
        if filtered_flights:
            return jsonify({"code": 200, "data": {"flights": filtered_flights}})

        return jsonify({"code": 404, "message": "No flights found matching the criteria."}), 404

    except Exception as e:
        # Catch and log unexpected errors
        print(f"An error occurred: {str(e)}")
        return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

@app.route("/flight/<string:flight_id>", methods=['GET'])
def get_flight_by_id(flight_id):
    try:
        flights = ref.get()

        # Handle list format
        if isinstance(flights, list):
            for flight in flights:
                if flight and flight.get("id") == int(flight_id):
                    flight['departureDate'] = format_date(flight['departureDate'])
                    return jsonify({"code": 200, "data": flight})
        else:
            return jsonify({"code": 500, "message": "Unexpected data structure in Firebase."}), 500

        return jsonify({"code": 404, "message": f"No flight found with id '{flight_id}'"}), 404

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
