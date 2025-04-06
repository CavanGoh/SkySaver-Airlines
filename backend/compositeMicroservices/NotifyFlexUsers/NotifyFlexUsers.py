# notifyflexusers.py
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])



FLIGHT_SERVICE_URL = "http://localhost:5000"
FLEXSEAT_SERVICE_URL = "http://localhost:5003"
NOTIFICATION_SERVICE_URL = "http://localhost:5021"

@app.route('/notify-flex-users', methods=['POST'])
def notify_flex_users():
    try:
        
        data = request.get_json()
        if not data or 'flight_id' not in data:
            return jsonify({"error": "Missing flight_id in request"}), 400
            
        flight_id = data['flight_id']

        
      
        try:
            
            flight_response = requests.get(f"{FLIGHT_SERVICE_URL}/flights")
            
            if flight_response.status_code != 200:
               
                return jsonify({"error": "Failed to fetch flights"}), 500
                
            flight_data = flight_response.json()
            
            if 'data' not in flight_data or 'flights' not in flight_data['data']:
               
                return jsonify({"error": "Unexpected flight service response format"}), 500
                
            
            flights = flight_data['data']['flights']
            
           
            if isinstance(flights, dict):
                flights = list(flights.values())
          
            flight_details = None
            for flight in flights:
                if str(flight.get('id')) == str(flight_id):
                    flight_details = flight
                    break
                    
            if not flight_details:
                
                return jsonify({"error": f"Flight with ID {flight_id} not found"}), 404
                
            
            
        except Exception as e:
            
            return jsonify({"error": f"Failed to fetch flight details: {str(e)}"}), 500
        
        
        try:
            flex_response = requests.get(
                f"{FLEXSEAT_SERVICE_URL}/flexseat/match",
                params={
                    "departure": flight_details['departure'],
                    "destination": flight_details['destination'],
                    "departureDate": flight_details['departureDate'],
                    "departureTime": flight_details.get('departureTime', '00:00:00')
                }
            )
           
            
            if flex_response.status_code != 200:
                return jsonify({
                    "error": f"Failed to fetch matching flex users. Status: {flex_response.status_code}",
                    "details": flex_response.text
                }), 500
                
            flex_data = flex_response.json()
            matching_users = flex_data.get('data', {}).get('userIds', [])
            
            if not matching_users:
                return jsonify({
                    "message": "No matching flex users found for this flight",
                    "users_notified": 0
                }), 200
                
            
            
        except Exception as e:
            
            return jsonify({"error": f"Failed to connect to flexseat service: {str(e)}"}), 500
        
        # Send notifications to matching users
        try:
            notification_data = {
                "users": matching_users,
                "flight_details": flight_details
            }
            
            notify_response = requests.post(
                f"{NOTIFICATION_SERVICE_URL}/send-notifications", 
                json=notification_data
            )
            
            
            
            if notify_response.status_code != 200:
                return jsonify({
                    "error": f"Failed to send notifications. Status: {notify_response.status_code}",
                    "details": notify_response.text
                }), 500
                
            return jsonify({
                "message": "Notifications sent successfully",
                "users_notified": len(matching_users),
                "users": matching_users
            }), 200
            
        except Exception as e:
           
            return jsonify({"error": f"Failed to connect to notification service: {str(e)}"}), 500
            
    except Exception as e:
        
        import traceback
       
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5020, debug=True)






