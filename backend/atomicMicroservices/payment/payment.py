from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
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
    paypal_payment_id = db.Column(db.String(100), nullable=True)  # Store PayPal payment ID
    paypal_sale_id = db.Column(db.String(100), nullable=True)     # Store PayPal sale ID for refunds
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


with app.app_context():
    try:
        # Try to add the paypal_payment_id column
        db.session.execute(text("ALTER TABLE payment ADD COLUMN paypal_payment_id VARCHAR(100)"))
        # Try to add the paypal_sale_id column
        db.session.execute(text("ALTER TABLE payment ADD COLUMN paypal_sale_id VARCHAR(100)"))
        db.session.commit()
         
    except Exception as e:
        db.session.rollback()
        print(f"Error altering table: {str(e)}")
    db.create_all()



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


# Normal booking payment endpoint
@app.route('/api/payment/normal', methods=['POST'])
def create_normal_payment():
    data = request.json
    required_fields = ['amount', 'user_id', 'booking_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Create PayPal payment
        paypal_payment = create_paypal_payment(
            data['amount'],
            f"{request.host_url}api/payment/success",
            f"{request.host_url}api/payment/cancel"
        )

        # Create payment record in database
        payment = Payment(
            amount=data['amount'],
            user_id=data['user_id'],
            booking_id=data['booking_id'],
            payment_type='normal',
            status='pending',
            paypal_payment_id=paypal_payment.id
        )
        db.session.add(payment)
        db.session.commit()

        # Find the approval URL
        approval_url = next((link.href for link in paypal_payment.links if link.rel == 'approval_url'), None)
        
        return jsonify({
            'payment_id': payment.id,
            'paypal_payment_id': paypal_payment.id,
            'paypal_approval_url': approval_url
        }), 201

    except Exception as e:
        print(f"Payment creation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Flex booking payment endpoint
@app.route('/api/payment/flex', methods=['POST'])
def create_flex_payment():
    data = request.json
    required_fields = ['amount', 'user_id', 'booking_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Create PayPal payment (same process as normal, but typically with discounted amount)
        paypal_payment = create_paypal_payment(
            data['amount'],  # This would be the discounted last-minute price
            f"{request.host_url}api/payment/success",
            f"{request.host_url}api/payment/cancel"
        )

        # Create payment record in database
        payment = Payment(
            amount=data['amount'],
            user_id=data['user_id'],
            booking_id=data['booking_id'],
            payment_type='flex',  # Mark as flex payment
            status='pending',
            paypal_payment_id=paypal_payment.id
        )
        db.session.add(payment)
        db.session.commit()

        # Find the approval URL
        approval_url = next((link.href for link in paypal_payment.links if link.rel == 'approval_url'), None)
        
        return jsonify({
            'payment_id': payment.id,
            'paypal_payment_id': paypal_payment.id,
            'paypal_approval_url': approval_url
        }), 201

    except Exception as e:
        print(f"Flex payment creation error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/payment/success', methods=['GET'])
def payment_success():
    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    
    app.logger.info(f"Payment success callback with payment_id: {payment_id}, payer_id: {payer_id}")
    
    try:
        # Execute the PayPal payment
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            # Find the sale ID for potential refunds
            sale_id = payment.transactions[0].related_resources[0].sale.id
            
            # Update our payment record
            db_payment = Payment.query.filter_by(paypal_payment_id=payment_id).first()
            if db_payment:
                db_payment.status = 'success'
                db_payment.paypal_sale_id = sale_id
                db.session.commit()
                
                return jsonify({
                    'status': 'success',
                    'message': 'Payment completed successfully',
                    'payment_id': db_payment.id
                })
            else:
                return jsonify({'error': 'Payment record not found'}), 404
        else:
            return jsonify({'error': payment.error}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/payment/cancel', methods=['GET'])
def payment_cancel():
    payment_id = request.args.get('paymentId')
    
    app.logger.info(f"Payment cancelled with payment_id: {payment_id}")
    
    # Update our payment record if it exists
    if payment_id:
        db_payment = Payment.query.filter_by(paypal_payment_id=payment_id).first()
        if db_payment:
            db_payment.status = 'cancelled'
            db.session.commit()
    
    # In a real application, you would redirect to a cancellation page
    return jsonify({
        'status': 'cancelled',
        'message': 'Payment was cancelled'
    })




# @app.route('/api/payments', methods=['GET'])
# def get_payments():
#     payments = Payment.query.all()
#     result = [{'id': p.id, 'amount': p.amount, 'status': p.status} for p in payments]
#     return jsonify(result)

@app.route('/api/payment/refund/<payment_id>', methods=['POST'])
def process_refund(payment_id):
    print(f"Attempting to refund payment with ID: {payment_id}")
    payment = Payment.query.get(payment_id)
    print(f"Query result: {payment}")
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404

    if payment.status != 'success':
        return jsonify({'error': f'Cannot refund payment with status: {payment.status}'}), 400

    try:
        if  payment.paypal_sale_id:
            sale = paypalrestsdk.Sale.find(payment.paypal_sale_id)
            refund = sale.refund({
                "amount": {
                    "total": str(payment.amount),
                    "currency": "SGD"
                }
            })
            
            if not refund.success():
                return jsonify({'error': 'PayPal refund failed: ' + str(refund.error)}), 500

        


        payment.status = 'refunded'
        db.session.commit()


        return jsonify({
            'payment_id': payment.id,
            'status': 'refunded'
        }), 200


    except Exception as e:
        return jsonify({'error': str(e)}), 500

#For debugging purpose 
@app.route('/api/payment/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    return jsonify({
        'id': payment.id,
        'amount': payment.amount,
        'user_id': payment.user_id,
        'booking_id': payment.booking_id,
        'payment_type': payment.payment_type,
        'status': payment.status,
        'paypal_payment_id': payment.paypal_payment_id,
        'paypal_sale_id': payment.paypal_sale_id,
        'created_at': payment.created_at,
        'updated_at': payment.updated_at
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)


