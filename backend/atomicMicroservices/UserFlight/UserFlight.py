from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/UserFlight'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class UserFlight(db.Model):
    __tablename__ = "UserFlight"
    user_id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, primary_key=True)

    def json(self):
        return {
            'user_id': self.user_id,
            'flight_id': self.flight_id,
        }

@app.route("/get/userflight/<string:user_id>")
def getUserFlights(user_id):
    user_id = int(user_id)
    flights = UserFlight.query.filter_by(user_id=user_id).all()
    return jsonify(
        {
                "code": 200,
                "data": {
                    "booking": [flight.json() for flight in flights]
                }
            }
    )

@app.route("/create/userflight", methods=['POST'])
def createUserFlight():
    try:
        data = request.get_json()
        
        if not all(key in data for key in ['user_id', 'flight_id']):
            return jsonify({
                "code": 400,
                "message": "Invalid request: missing required fields - 'user_id' and 'flight_id' required"
            }), 400
        
        user_id = int(data['user_id'])
        flight_id = int(data['flight_id'])
        
        existing = UserFlight.query.filter_by(user_id=user_id, flight_id=flight_id).first()
        if existing:
            return jsonify({
                "code": 400,
                "message": "User flight association already exists"
            }), 400
        
        new_userflight = UserFlight(user_id=user_id, flight_id=flight_id)
        
        db.session.add(new_userflight)
        db.session.commit()
        
        return jsonify({
            "code": 201,
            "data": new_userflight.json(),
            "message": "User flight booking created successfully"
        }), 201
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred while creating the booking: {str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)