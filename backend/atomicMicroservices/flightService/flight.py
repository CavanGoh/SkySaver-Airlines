import os
import base64
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)

CORS(app)


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
    'databaseURL': 'https://skysaver-db-default-rtdb.firebaseio.com/'  # Replace with your RTDB URL
})

# Connect to RTDB
ref = db.reference("flights")  # Reference to the "flights" node in RTDB

# Get all flights
@app.route("/flights", methods=['GET'])
def get_all_flights():
    flights = ref.get()  # Fetches all flights under the "flights" node
    if flights:
        return jsonify({"code": 200, "data": {"flights": flights}})
    return jsonify({"code": 404, "message": "No flights found."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
