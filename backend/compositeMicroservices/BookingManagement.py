from flask import Flask, request, jsonify, Blueprint
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])



booking_management = Blueprint('booking_management', __name__)


# Service URLs - these would typically be in config.py
FLIGHT_SERVICE_URL = os.environ.get('FLIGHT_SERVICE_URL', 'http://localhost:5000/flights')

PAYMENT_SERVICE_URL = os.environ.get('PAYMENT_SERVICE_URL', 'http://127.0.0.1:5005/api/payment/flex')

SEAT_SERVICE_URL = os.environ.get('SEAT_SERVICE_URL', 'http://127.0.0.1:8080/seats')

FLEX_SERVICE_URL = os.environ.get('FLEX_SERVICE_URL', 'http://localhost:5003/flexseat')

BOOKING_SERVICE_URL = os.environ.get('BOOKING_SERVICE_URL', 'http://localhost:5001/booking')

OUTSYSTEMS_PRICE_URL = 'https://personal-y0j5ezns.outsystemscloud.com/Price/rest/PriceAPI/CalculatePrice'


@booking_management.route('/api/booking/accept', methods=['POST'])
def accept_booking():
    data = request.json
    
    if not data or 'user_id' not in data or 'flight_id' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    try:
        # Get flight information
        flight_response = requests.get(f"{FLIGHT_SERVICE_URL}?id={data['flight_id']}")
        flight_response.raise_for_status()
        flight_data = flight_response.json()['data']['flights'][0]
        
        # Calculate discounted price
        price_request_data = {
            "basePrice": flight_data['price']
        }
        price_response = requests.post(OUTSYSTEMS_PRICE_URL, json=price_request_data)
        price_response.raise_for_status()
        discounted_price = price_response.json()['FinalPrice']
        
        return jsonify({
            'booking_id': f"temp_{data['user_id']}",
            'user_id': data['user_id'],
            'flight_id': data['flight_id'],
            'departure': flight_data['departure'],
            'destination': flight_data['destination'],
            'original_price': flight_data['price'],
            'discounted_price': discounted_price,
            'currency': 'USD',  # Assuming USD, adjust if needed
            'status': 'price_calculated',
            'next_step': 'payment'
        }), 200
        
    except requests.RequestException as e:
        return jsonify({'error': f'Error communicating with services: {str(e)}'}), 500



@booking_management.route('/api/booking/process-payment', methods=['POST'])
def process_payment():
    try:
        data = request.json
        # Validate request data
        if not data or 'user_id' not in data or 'booking_id' not in data or 'price' not in data:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Log the data for debugging
        print(f"Processing payment: {data}")
        
        # Prepare payment request
        payment_data = {
            'amount': data['price'],
            'user_id': data['user_id'],
            'booking_id': data['booking_id']
        }
        
        # Log the payment URL
        print(f"Sending request to: {PAYMENT_SERVICE_URL}")
        
        # Send payment request to payment service
        response = requests.post(PAYMENT_SERVICE_URL, json=payment_data)
        response.raise_for_status()
        
        # Get payment response
        payment_result = response.json()
        
        return jsonify({
            'payment_id': payment_result['payment_id'],
            'paypal_payment_id': payment_result['paypal_payment_id'],
            'paypal_approval_url': payment_result['paypal_approval_url'],
            'status': 'payment_initiated',
            'next_step': 'confirm_payment'
        }), 200
    except requests.RequestException as e:
        print(f"Request error: {str(e)}")
        return jsonify({'error': f'Error processing payment: {str(e)}'}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


def update_seat_availability(flight_id, seat_id, availability):
    """
    Update the availability of a seat in the seat service.
    """
    url = f"{SEAT_SERVICE_URL}/{flight_id}/{seat_id}/availability"
    params = {"availability": availability}
    
    try:
        response = requests.put(url, params=params)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Error updating seat availability: {str(e)}")
        return False

@booking_management.route('/api/booking/confirm', methods=['POST'])
def confirm_booking():
    data = request.json
    
    # Validate request data for both seat and flex user information
    required_fields = ['flight_id', 'seat_id', 'userId', 'startDestination', 
                      'endDestination', 'startDateTime', 'endDateTime']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required parameters', 
                       'required_fields': required_fields}), 400
    
    # Step 1: Update seat availability
    seat_updated = update_seat_availability(data['flight_id'], data['seat_id'], False)
    
    # Step 2: Remove user from flex list
    flex_data = {
        'userId': data['userId'],
        'startDestination': data['startDestination'],
        'endDestination': data['endDestination'],
        'startDateTime': data['startDateTime'],
        'endDateTime': data['endDateTime']
    }
    
    try:
        flex_response = requests.delete(f"{FLEX_SERVICE_URL}/delete", json=flex_data)
        flex_user_removed = flex_response.status_code == 200
        flex_response_data = flex_response.json()
    except Exception as e:
        flex_user_removed = False
        flex_response_data = {'error': str(e)}
    
    # Step 3: Create booking record
    booking_created = False
    booking_data = {}
    
    if seat_updated:  # Only create booking if seat was updated successfully
        try:
            booking_request = {
                'user_id': data['userId'],  # Use userId from the request
                'flight_id': data['flight_id']
            }
            
            booking_response = requests.post(f"{BOOKING_SERVICE_URL}/new", json=booking_request)
            
            if booking_response.status_code in [201, 409]:  # Success or already exists
                booking_created = True
                booking_data = booking_response.json().get('data', {})
            else:
                print(f"Booking creation failed: {booking_response.text}")
        except Exception as e:
            print(f"Error creating booking: {str(e)}")
    
    # Determine overall success based on all operations
    if seat_updated and flex_user_removed and booking_created:
        return jsonify({
            'status': 'confirmed',
            'message': 'Flex booking confirmed: seat reserved, user removed from flex list, and booking created',
            'flight_id': data['flight_id'],
            'seat_id': data['seat_id'],
            'booking': booking_data,
            'flex_data': flex_response_data.get('data', {})
        }), 200
    elif seat_updated and booking_created:
        return jsonify({
            'status': 'partial_success',
            'message': 'Seat reserved and booking created, but failed to remove user from flex list',
            'flight_id': data['flight_id'],
            'seat_id': data['seat_id'],
            'booking': booking_data,
            'flex_error': flex_response_data.get('message', 'Unknown error')
        }), 207
    elif seat_updated:
        return jsonify({
            'status': 'partial_success',
            'message': 'Seat reserved but failed to create booking and/or remove user from flex list',
            'flight_id': data['flight_id'],
            'seat_id': data['seat_id']
        }), 207
    else:
        return jsonify({
            'status': 'failed',
            'message': 'Unable to reserve seat. Booking not confirmed.'
        }), 500

if __name__ == '__main__':
    app.register_blueprint(booking_management)
    app.run(host='0.0.0.0', port=5090, debug=True)


# Additional endpoints will be added for payment processing, seat updates, etc.
