from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/flexSeat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class FlexSeat(db.Model):
    __tablename__ = 'flexSeat'
    passengerId = db.Column(db.Integer, primary_key=True)
    startDestination = db.Column(db.String(100), primary_key=True)
    endDestination = db.Column(db.String(100), primary_key=True)
    startDateTime = db.Column(db.DateTime, primary_key=True)
    endDateTime = db.Column(db.DateTime, primary_key=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def json(self):
        return {
        'passengerId': self.passengerId,
        'startDestination': self.startDestination,
        'endDestination': self.endDestination,
        'startDateTime': self.startDateTime.strftime('%Y-%m-%d %H:%M:%S'),
        'endDateTime': self.endDateTime.strftime('%Y-%m-%d %H:%M:%S'),
        'createdAt': self.createdAt.strftime('%Y-%m-%d %H:%M:%S')
        }


@app.route('/flexseat', methods=['GET'])
def get_all_flexseats():
    passenger_id = request.args.get('passengerId')
    if passenger_id:
        ## if passengerId is passed as a query param, filter using it
        ## if not, return all records
        records = FlexSeat.query.filter_by(passengerId=passenger_id).all()
    else:
        records = FlexSeat.query.all()

    return jsonify({
        "code": 200,
        "data": [record.json() for record in records]
    })

## to create a new search
@app.route('/flexseat/new', methods=['POST'])
def create_flexseat():
    try:
        data = request.get_json()
        ## converts the input JSON into a FlexSeat object
        new_record = FlexSeat(
            passengerId=data['passengerId'],
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
        record = FlexSeat.query.filter_by(
            passengerId=data['passengerId'],
            startDestination=data['startDestination'],
            endDestination=data['endDestination'],
            startDateTime=datetime.strptime(data['startDateTime'], '%Y-%m-%d %H:%M:%S'),
            endDateTime=datetime.strptime(data['endDateTime'], '%Y-%m-%d %H:%M:%S')
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
        return jsonify({
            "code": 500,
            "message": f"An error occurred: {str(e)}"
        }), 500


## run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)