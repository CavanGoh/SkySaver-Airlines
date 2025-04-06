from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime,timezone


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
    startDateTime = db.Column(db.DateTime, primary_key=True)
    endDateTime = db.Column(db.DateTime, primary_key=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def json(self):
        return {
        'userId': self.userId,
        'startDestination': self.startDestination,
        'endDestination': self.endDestination,
        'startDateTime': self.startDateTime.strftime('%Y-%m-%d %H:%M:%S'),
        'endDateTime': self.endDateTime.strftime('%Y-%m-%d %H:%M:%S'),
        'createdAt': self.createdAt.strftime('%Y-%m-%d %H:%M:%S')
        }


@app.route('/flexseat', methods=['GET'])
def get_all_flexseats():
    user_id = request.args.get('userId')
    if user_id:
        ## if userId is passed as a query param, filter using it
        ## if not, return all records
        records = FlexSeat.query.filter_by(userId=user_id).all()
    else:
        records = FlexSeat.query.all()

    return jsonify({
        "code": 200,
        "data": [record.json() for record in records]
    })


#WK added
@app.route('/flexseat/match', methods=['GET'])
def get_cancelled_match():
    try:
        departure = request.args.get('departure')
        destination = request.args.get('destination')
        departure_date_str = request.args.get('departureDate')
        departure_time_str = request.args.get('departureTime', '00:00:00')  # Default to start of day if not provided
        
        # Input validation
        if not all([departure, destination, departure_date_str]):
            return jsonify({
                "code": 400,
                "message": "Missing required parameters: departure, destination, departureDate"
            }), 400
        
        # Convert the departure date string to a datetime object
        try:
            # Check if time is already included in the date string
            if 'T' in departure_date_str or ' ' in departure_date_str:
                departure_datetime = datetime.fromisoformat(departure_date_str.replace('T', ' '))
            else:
                # Combine date and time
                departure_datetime = datetime.strptime(
                    f"{departure_date_str} {departure_time_str}", 
                    '%Y-%m-%d %H:%M:%S'
                )
        except ValueError:
            # Try alternate date format (MM-DD-YYYY)
            try:
                if '-' in departure_date_str:
                    parts = departure_date_str.split('-')
                    if len(parts[0]) == 2:  # MM-DD-YYYY format
                        departure_date_str = f"{parts[2]}-{parts[0]}-{parts[1]}"
                departure_datetime = datetime.strptime(
                    f"{departure_date_str} {departure_time_str}", 
                    '%Y-%m-%d %H:%M:%S'
                )
            except ValueError as e:
                return jsonify({
                    "code": 400,
                    "message": f"Invalid date format: {str(e)}"
                }), 400
        
        print(f"Searching for matches: {departure} → {destination} on {departure_datetime}")
        
        # Query the database for matching FlexSeat records
        matches = FlexSeat.query.filter(
            FlexSeat.startDestination == departure,
            FlexSeat.endDestination == destination,
            FlexSeat.startDateTime <= departure_datetime,
            FlexSeat.endDateTime >= departure_datetime
        ).all()
        
        matched_user_ids = [match.userId for match in matches]
        
        # Return only the matched userIds
        return jsonify({
            "code": 200,
            "data": {
                "userIds": matched_user_ids,
                "count": len(matched_user_ids),
                "searchCriteria": {
                    "departure": departure,
                    "destination": destination,
                    "departureDateTime": departure_datetime.strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500


## to create a new search
@app.route('/flexseat/new', methods=['POST'])
def create_flexseat():
    try:
        data = request.get_json()
        ## converts the input JSON into a FlexSeat object


         # Validate required fields
        required_fields = ['userId', 'startDestination', 'endDestination', 'startDateTime', 'endDateTime']
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
            startDateTime=datetime.strptime(data['startDateTime'], '%Y-%m-%d %H:%M:%S'),
            endDateTime=datetime.strptime(data['endDateTime'], '%Y-%m-%d %H:%M:%S')
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

## to remove a flex seat record
@app.route('/flexseat/delete', methods=['DELETE'])
def delete_flexseat():
    try:
        data = request.get_json()
        start_date = datetime.fromisoformat(data['startDateTime'].replace('Z', '+00:00')).replace(tzinfo=timezone.utc)
        end_date = datetime.fromisoformat(data['endDateTime'].replace('Z', '+00:00')).replace(tzinfo=timezone.utc)
        
        record = FlexSeat.query.filter_by(
            userId=data['userId'],
            startDestination=data['startDestination'],
            endDestination=data['endDestination'],
            startDateTime=start_date,
            endDateTime=end_date
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
        print(f"Error in delete_flexseat: {str(e)}")  # Add this line for debugging
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500


## run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)