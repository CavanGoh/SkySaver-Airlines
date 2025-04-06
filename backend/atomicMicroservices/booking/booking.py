from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

import os
from os import environ

app = Flask(__name__)
# CORS(app)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])


from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

db_base = os.getenv("hostdbURL")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    # db_base + "/booking"
    # if db_base else 
    "mysql+mysqlconnector://root@host.docker.internal:3306/booking"
)#checks in the ".env" file for "dbURL"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/booking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Booking(db.Model):
    __tablename__ = "booking"
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    flight_id = db.Column(db.Integer, nullable=False)
    seat_id= db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def json(self):
        return {
            'booking_id': self.booking_id,
            'user_id': self.user_id,
            'flight_id': self.flight_id,
            'seat_id': self.seat_id,
            'status': self.status,
        }

@app.route("/booking/<string:user_id>")
def get_all_booking(user_id):
    user_id = int(user_id)
    bookings = db.session.query(Booking).filter_by(user_id=user_id).all()
    return jsonify({
        "code": 200,
        "data": {
            "booking": [booking.json() for booking in bookings]
        }
    })
    
@app.route("/booking/cancel/<string:booking_id>", methods=['PUT'])
def cancel_booking(booking_id):
        booking_id = int(booking_id)
        
        booking = db.session.get(Booking, booking_id)
        
        if not booking:
            return jsonify({
                "code": 404,
                "message": f"Booking {booking_id} not found."
            }), 404
            
        if booking.status == "Cancelled":
            return jsonify({
                "code": 400,
                "message": f"Booking is already cancelled."
            }), 400
        
            
        booking.status = "Cancelled"
        
        db.session.commit()
        
        return jsonify({
            "code": 200,
            "data": {
                "booking": booking.json(),
                "message": "Booking successfully cancelled."
            }
        })
        
@app.route("/booking/new", methods=['POST'])
def new_booking():
    try:
        data = request.get_json()
        
        existing_booking = db.session.query(Booking).filter_by(
            user_id=data['user_id'], 
            flight_id=data['flight_id'],
            seat_id=data['seat_id']
        ).first()
        
        if existing_booking:
            if existing_booking.status == "Confirmed":
                return jsonify({
                    "code": 409, 
                    "data": {
                        "booking": existing_booking.json()
                    },
                    "message": "User already has a booking for this flight."
                }), 409
                
            
        new_booking = Booking(
            user_id=data['user_id'],
            flight_id=data['flight_id'],
            seat_id=data['seat_id'],
            status="Confirmed"
        )
        
        db.session.add(new_booking)
        db.session.commit()
        
        return jsonify({
            "code": 201,
            "data": {
                "booking": new_booking.json(),
                "message": "Booking created successfully."
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500, 
            "message": f"An error occurred: {str(e)}"
        }), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)