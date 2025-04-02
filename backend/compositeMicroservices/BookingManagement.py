from flask import Flask, request, jsonify, Blueprint
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

booking_management = Blueprint('booking_management', __name__)

# Service URLs - these would typically be in config.py
PRICE_SERVICE_URL = os.environ.get('PRICE_SERVICE_URL', 'http://localhost:5002/api/price')

PAYMENT_SERVICE_URL = os.environ.get('PAYMENT_SERVICE_URL', 'http://127.0.0.1:5000/api/payment/flex')





@booking_management.route('/api/booking/accept', methods=['POST'])
def accept_booking():
    """
    Handle booking acceptance from UI:
    1. Receive booking acceptance
    2. Get price from price service
    """
    data = request.json
    
    # Validate request data
    if not data or 'user_id' not in data or 'flight_id' not in data or 'destination' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Step 2: Send request to Price service
    try:
        price_request_data = {
            'user_id': data['user_id'],
            'flight_id': data['flight_id'],
            'destination': data['destination'],
            'bookingType': data.get('bookingType', 'standard')
        }
        
        response = requests.post(PRICE_SERVICE_URL, json=price_request_data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Step 3: Receive price from Price service
        price_data = response.json()
        
        # Return price information to the UI
        return jsonify({
            'booking_id': data.get('booking_id', 'temp_' + str(data['user_id'])),
            'user_id': data['user_id'],
            'flight_id': data['flight_id'],
            'destination': data['destination'],
            'price': price_data['price'],
            'currency': price_data['currency'],
            'status': 'price_calculated',
            'next_step': 'payment'
        }), 200
        
    except requests.RequestException as e:
        return jsonify({'error': f'Error communicating with price service: {str(e)}'}), 500


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

if __name__ == '__main__':
    app.run(debug=True)


# Additional endpoints will be added for payment processing, seat updates, etc.
