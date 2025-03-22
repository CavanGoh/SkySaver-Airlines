from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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

@app.route("/userflight/<string:user_id>")
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)