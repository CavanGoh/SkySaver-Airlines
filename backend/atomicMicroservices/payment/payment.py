from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@host.docker.internal:3306/payment_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Payment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(36), nullable=False)
    status = db.Column(db.String(20), default='pending')


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return "Payment Service is Running lesgo!"

@app.route('/api/payment', methods=['POST'])
def create_payment():
    """Handle payment creation"""
    data = request.json

    if not data or 'amount' not in data or 'user_id' not in data:
        return jsonify({'error': 'Invalid payment data'}), 400


    payment = Payment(
        amount=data['amount'],
        user_id=data['user_id'],
        status='pending'  
    )

 
    db.session.add(payment)
    db.session.commit()
    
    #PAYPAL API add later
    
    payment.status = 'success'  
    db.session.commit()

    return jsonify({'payment_id': payment.id, 'status': payment.status}), 201


@app.route('/api/payment/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    """Fetch payment details"""
    payment = Payment.query.get(payment_id)

    if not payment:
        return jsonify({'error': 'Payment not found'}), 404

    return jsonify({
        'payment_id': payment.id,
        'amount': payment.amount,
        'user_id': payment.user_id,
        'status': payment.status
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

