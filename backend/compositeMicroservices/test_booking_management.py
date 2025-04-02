import pytest
import json
from flask import Flask
import os
from unittest.mock import patch, MagicMock

# Import the blueprint
from BookingManagement import booking_management


@pytest.fixture
def client():
    """Create a test client for the app."""
    app = Flask(__name__)
    app.register_blueprint(booking_management)
    with app.test_client() as client:
        yield client

def test_accept_booking_success(client):
    """Test successful booking acceptance."""
    # Mock the price service response
    mock_price_response = MagicMock()
    mock_price_response.json.return_value = {"price": 420.0, "currency": "SGD"}
    mock_price_response.raise_for_status.return_value = None
    
    with patch('requests.post') as mock_post:
        mock_post.return_value = mock_price_response
        
        # Test data
        data = {
            "user_id": "user123",
            "flight_id": "flight456",
            "destination": "Singapore",
            "bookingType": "flex seat"
        }
        
        # Make request
        response = client.post('/api/booking/accept', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['user_id'] == "user123"
        assert response_data['flight_id'] == "flight456"
        assert response_data['destination'] == "Singapore"
        assert response_data['price'] == 420.0
        assert response_data['currency'] == "SGD"
        assert response_data['status'] == "price_calculated"
        assert response_data['next_step'] == "payment"

def test_accept_booking_missing_params(client):
    """Test booking acceptance with missing parameters."""
    # Test data with missing required field
    data = {
        "user_id": "user123",
        "flight_id": "flight456"
        # Missing destination
    }
    
    # Make request
    response = client.post('/api/booking/accept', 
                         data=json.dumps(data),
                         content_type='application/json')
    
    # Assertions
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert 'error' in response_data

def test_process_payment_success(client):
    """Test successful payment processing."""
    # Mock the payment service response
    mock_payment_response = MagicMock()
    mock_payment_response.json.return_value = {
        "payment_id": "pay123",
        "paypal_payment_id": "PAYID-123456",
        "paypal_approval_url": "https://www.sandbox.paypal.com/checkout/123"
    }
    mock_payment_response.raise_for_status.return_value = None
    
    with patch('requests.post') as mock_post:
        mock_post.return_value = mock_payment_response
        
        # Test data
        data = {
            "user_id": "user123",
            "booking_id": "temp_user123",
            "price": 420.0
        }
        
        # Make request
        response = client.post('/api/booking/process-payment', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        # Assertions
        assert response.status_code == 200
        response_data = json.loads(response.data)
        assert response_data['payment_id'] == "pay123"
        assert response_data['paypal_payment_id'] == "PAYID-123456"
        assert "paypal.com" in response_data['paypal_approval_url']
        assert response_data['status'] == "payment_initiated"
        assert response_data['next_step'] == "confirm_payment"
