from flask import Flask, request, jsonify, Blueprint
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])



booking_management = Blueprint('booking_management', __name__)


# Service URLs - these would typically be in config.py
# Flight service is containerized, use container name
FLIGHT_SERVICE_URL = os.environ.get('FLIGHT_SERVICE_URL', 'http://flight:5000/flights')

# Payment service is not containerized, use host.docker.internal
PAYMENT_SERVICE_URL = os.environ.get('PAYMENT_SERVICE_URL', 'http://host.docker.internal:5005/api/payment/flex')

# Seat service is containerized, use container name
SEAT_SERVICE_URL = os.environ.get('SEAT_SERVICE_URL', 'http://seat:8080/seats')

# FlexSeat service is not containerized, use host.docker.internal
FLEX_SERVICE_URL = os.environ.get('FLEX_SERVICE_URL', 'http://host.docker.internal:5003')

# Booking service is not containerized, use host.docker.internal
BOOKING_SERVICE_URL = os.environ.get('BOOKING_SERVICE_URL',  "http://booking:5001/booking")

# External service, keep the full URL
OUTSYSTEMS_PRICE_URL = 'https://personal-y0j5ezns.outsystemscloud.com/Price/rest/PriceAPI/CalculatePrice'

BOOK_FLIGHT_COMPOSITE_URL = os.environ.get('BOOK_FLIGHT_URL', 'http://book-flight:5002/book_flight')


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


# def update_seat_availability(flight_id, seat_id, availability):
#     """
#     Update the availability of a seat in the seat service.
#     """
#     url = f"{SEAT_SERVICE_URL}/{flight_id}/{seat_id}/availability"
    
#     try:
#         # Send availability in the request body as JSON, not as a query parameter
#         response = requests.put(url, json={"availability": availability})
#         response.raise_for_status()
#         return True
#     except requests.RequestException as e:
#         print(f"Error updating seat availability: {str(e)}")
#         return False


@booking_management.route('/api/booking/confirm', methods=['POST'])
def confirm_booking():
    data = request.json
    
    # Validate request data for both seat and flex user information
    required_fields = ['flight_id', 'seat_id', 'userId', 'startDestination', 
                      'endDestination', 'startDate', 'endDate']
    
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required parameters', 
                       'required_fields': required_fields}), 400
    
    bookFlightResponse = requests.post(BOOK_FLIGHT_COMPOSITE_URL,json={ 
        "user_id": data['userId'],
        "flight_id": data['flight_id'],
        "seat_id": data['seat_id']
    })
    print("Flight response")
    print(bookFlightResponse.json())

    
    # Step 2: Remove user from flex list
    flex_data = {
        'userId': data['userId'],
        'startDestination': data['startDestination'],
        'endDestination': data['endDestination'],
        'startDate': data['startDate'],
        'endDate': data['endDate']
    }
    
    try:
        flex_response = requests.delete(f"{FLEX_SERVICE_URL}/delete", json=flex_data)
        flex_user_removed = flex_response.status_code == 200
        flex_response_data = flex_response.json()
    except Exception as e:
        flex_user_removed = False
        flex_response_data = {'error': str(e)}
    
    # Determine overall success based on all operations
    if bookFlightResponse.status_code == 200 and flex_user_removed:
        return jsonify({
            'status': 'confirmed',
            'message': 'Flex booking confirmed: seat reserved, user removed from flex list, and booking created',
            'flight_id': data['flight_id'],
            'seat_id': data['seat_id'],
            'booking': bookFlightResponse.json(),
            'flex_data': flex_response_data
        }), 200
    elif bookFlightResponse.status_code == 200:
        return jsonify({
            'status': 'partial_success',
            'message': 'Seat reserved and booking created, but failed to remove user from flex list',
            'flight_id': data['flight_id'],
            'seat_id': data['seat_id'],
            'booking': bookFlightResponse.json(),
            'flex_error': flex_response_data.get('message', 'Unknown error')
        }), 207
    else:
        return jsonify({
            'status': 'failed',
            'message': 'Unable to reserve seat. Booking not confirmed.',
            'booking_error': bookFlightResponse.json().get('message', 'Unknown error')
        }), 500

if __name__ == '__main__':
    app.register_blueprint(booking_management)
    app.run(host='0.0.0.0', port=5090, debug=True)


# Additional endpoints will be added for payment processing, seat updates, etc.
