from flask import Flask, request, jsonify

app = Flask(__name__)

# Price calculation logic
def calculate_price(destination, booking_type):
    """Calculate seat price based on destination and booking type"""
    # Base prices for different destinations
    base_prices = {
        "New York": 500.0,
        "London": 450.0,
        "Tokyo": 800.0,
        "Paris": 480.0,
        "Sydney": 900.0,
        "Dubai": 650.0,
        "Singapore": 700.0,
        "Rome": 470.0,
    }
    
    # Default price if destination not found
    base_price = base_prices.get(destination, 400.0)
    
    # Apply booking type modifier
    if booking_type.lower() == "flex seat":
        # Flex seat gets 40% discount
        return base_price * 0.60
    else:
        # Standard economy seat
        return base_price

@app.route('/')
def home():
    return "Price Service is Running!"

@app.route('/api/price', methods=['POST'])
def get_price():
    """Calculate and return price based on provided parameters"""
    data = request.json
    
    # Validate request data
    if not data or 'user_id' not in data or 'flight_id' not in data or 'destination' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    destination = data['destination']
    booking_type = data.get('bookingType', 'standard')
    
    # Calculate price
    price = calculate_price(destination, booking_type)
    
    return jsonify({
        'price': price,
        'currency': 'USD'
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)