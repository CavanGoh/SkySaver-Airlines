from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/flexSeat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class FlexSeat(db.Model):
    __tablename__ = 'flexSeat'
    userId = db.Column(db.Integer, primary_key=True)
    startDestination = db.Column(db.String(100), primary_key=True)
    endDestination = db.Column(db.String(100), primary_key=True)
    startDate = db.Column(db.Date, primary_key=True)  # Changed from DateTime to Date
    endDate = db.Column(db.Date, primary_key=True)    # Changed from DateTime to Date
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def json(self):
        return {
            'userId': self.userId,
            'startDestination': self.startDestination,
            'endDestination': self.endDestination,
            'startDate': self.startDate.strftime('%Y-%m-%d'),  # Format as Date
            'endDate': self.endDate.strftime('%Y-%m-%d'),      # Format as Date
            'createdAt': self.createdAt.strftime('%Y-%m-%d %H:%M:%S')
        }

@app.route('/flexseat', methods=['GET'])
def get_all_flexseats():
    user_id = request.args.get('userId')
    if user_id:
        records = FlexSeat.query.filter_by(userId=user_id).all()
    else:
        records = FlexSeat.query.all()

    return jsonify({
        "code": 200,
        "data": [record.json() for record in records]
    })

@app.route('/flexseat/match', methods=['GET'])
def get_cancelled_match():
    try:
        departure = request.args.get('departure')
        destination = request.args.get('destination')
        departure_date_str = request.args.get('departureDate')
        
        if not all([departure, destination, departure_date_str]):
            return jsonify({
                "code": 400,
                "message": "Missing required parameters: departure, destination, departureDate"
            }), 400

        departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d')
        departure_date = departure_date.date()  # Convert to date object

        print(f"Searching for matches: {departure} → {destination} on {departure_date}")

        matches = FlexSeat.query.filter(
            FlexSeat.startDestination == departure,
            FlexSeat.endDestination == destination,
            FlexSeat.startDate <= departure_date,
            FlexSeat.endDate >= departure_date
        ).all()

        matched_user_ids = [match.userId for match in matches]

        return jsonify({
            "code": 200,
            "data": {
                "userIds": matched_user_ids,
                "count": len(matched_user_ids),
                "searchCriteria": {
                    "departure": departure,
                    "destination": destination,
                    "departureDate": departure_date.strftime('%Y-%m-%d')
                }
            }
        })

    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500

@app.route('/flexseat/new', methods=['POST'])
def create_flexseat():
    try:
        data = request.get_json()

        required_fields = ['userId', 'startDestination', 'endDestination', 'startDate', 'endDate']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({
                "code": 400,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        new_record = FlexSeat(
            userId=data['userId'],
            startDestination=data['startDestination'],
            endDestination=data['endDestination'],
            startDate=datetime.strptime(data['startDate'], '%Y-%m-%d').date(),  # Changed to Date
            endDate=datetime.strptime(data['endDate'], '%Y-%m-%d').date(),       # Changed to Date
        )

        db.session.add(new_record)
        db.session.commit()

        return jsonify({
            "code": 201,
            "message": "Flex seat preference created successfully.",
            "data": new_record.json()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500

@app.route('/flexseat/delete', methods=['DELETE'])
def delete_flexseat():
    try:
        data = request.get_json()
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d').date()  # Changed to Date
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d').date()       # Changed to Date

        record = FlexSeat.query.filter_by(
            userId=data['userId'],
            startDestination=data['startDestination'],
            endDestination=data['endDestination'],
            startDate=start_date,
            endDate=end_date
        ).first()

        if not record:
            return jsonify({
                "code": 404,
                "message": "Flex seat preference not found."
            }), 404

        db.session.delete(record)
        db.session.commit()

        return jsonify({
            "code": 200,
            "message": "Flex seat preference deleted successfully.",
            "data": record.json()
        })
    except Exception as e:
        db.session.rollback()
        print(f"Error in delete_flexseat: {str(e)}")
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
