from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid
import paypalrestsdk
import os





app = Flask(__name__)


CORS(app)  # Enable CORS for all routes


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@host.docker.internal:3306/payment_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


# PayPal Configuration
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" in production
    "client_id": os.getenv('PAYPAL_CLIENT_ID','AXsLZUMGGj-Xf-POACA7Uyj1ptp3oR44M-vtFNYpmrXS7uZC98P16m8aVUvV5-_79MotkUQIn5WFBRhO'),
    "client_secret": os.getenv('PAYPAL_CLIENT_SECRET' , 'EKSyc8AlOnLfzNV7-Z_hswCEVikl9RaUIF8mNgpyVbMiWwxOUTWkcXNKwgGLWuqaQJ0fZ_4AMsAxQZAJ')
})


class Payment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    booking_id = db.Column(db.String(36), nullable=False)
    payment_type = db.Column(db.String(20), nullable=False)  # 'normal' or 'flex'
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


with app.app_context():
    db.create_all()


# Create Payment
def create_paypal_payment(amount, return_url, cancel_url):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": return_url,
            "cancel_url": cancel_url
        },
        "transactions": [{
            "amount": {
                "total": str(amount),
                "currency": "SGD"
            },
            "description": "Flight Booking Payment"
        }]
    })
    if payment.create():
        return payment
    else:
        raise Exception(payment.error)


@app.route('/api/payment/normal', methods=['POST'])
def create_normal_payment():
    data = request.json
    required_fields = ['amount', 'user_id', 'booking_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400


    try:
        paypal_payment = create_paypal_payment(
            data['amount'],
            f"{request.host_url}payment/success",
            f"{request.host_url}payment/cancel"
        )


        payment = Payment(
            amount=data['amount'],
            user_id=data['user_id'],
            booking_id=data['booking_id'],
            payment_type='normal',
            status='pending'
        )
        db.session.add(payment)
        db.session.commit()


        return jsonify({
            'payment_id': payment.id,
            'paypal_approval_url': paypal_payment.links[1].href
        }), 201


    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/payment/flex', methods=['POST'])
def create_flex_payment():
    data = request.json
    required_fields = ['amount', 'user_id', 'booking_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400


    try:
        payment = Payment(
            amount=data['amount'],
            user_id=data['user_id'],
            booking_id=data['booking_id'],
            payment_type='flex',
            status='pending'
        )
        db.session.add(payment)
        db.session.commit()


        return jsonify({
            'payment_id': payment.id,
            'status': 'pending'
        }), 201


    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    result = [{'id': p.id, 'amount': p.amount, 'status': p.status} for p in payments]
    return jsonify(result)

@app.route('/api/payment/refund/<payment_id>', methods=['POST'])
def process_refund(payment_id):
    print(f"Attempting to refund payment with ID: {payment_id}")
    payment = Payment.query.get(payment_id)
    print(f"Query result: {payment}")
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404

    try:
        if payment.payment_type == 'normal':
            #The paypal refund api i will add later
            pass


        payment.status = 'refunded'
        db.session.commit()


        return jsonify({
            'payment_id': payment.id,
            'status': 'refunded'
        }), 200


    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


