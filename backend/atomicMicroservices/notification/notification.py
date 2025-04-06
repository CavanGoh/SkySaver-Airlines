from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

# Database configuration - dedicated notification database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/notification_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Notification model
class Notification(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, nullable=False)
    flight_id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    seen = db.Column(db.Boolean, default=False)
    seen_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "flight_id": self.flight_id,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
            "seen": self.seen,
            "seen_at": self.seen_at.isoformat() if self.seen_at else None,
            "is_active": self.is_active
        }

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/send-notifications', methods=['POST'])
def send_notifications():
    data = request.json
    users = data['users']
    flight_details = data['flight_details']

    notifications = []
    for user in users:
        notification = Notification(
            user_id=user,
            flight_id=flight_details['id'],
            message=f"Flight {flight_details['id']} from {flight_details['departure']} to {flight_details['destination']} on {flight_details['departureDate']} was cancelled. You may now book."
        )
        db.session.add(notification)
        notifications.append(notification)

    db.session.commit()

    return jsonify({
        "message": "Notifications sent", 
        "count": len(notifications)
    }), 200

@app.route('/notifications', methods=['GET'])
def get_notifications():
    user_id = request.args.get('user_id')
    
    query = Notification.query.filter_by(is_active=True)
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    notifications = query.order_by(Notification.created_at.desc()).all()
    
    return jsonify([notification.to_dict() for notification in notifications]), 200

@app.route('/notifications/mark-seen', methods=['PUT'])
def mark_notification_seen():
    data = request.json
    notification_id = data.get('notification_id')
    
    if not notification_id:
        return jsonify({"error": "Missing notification_id"}), 400
        
    notification = Notification.query.get(notification_id)
    
    if not notification:
        return jsonify({"error": "Notification not found"}), 404
        
    notification.seen = True
    notification.seen_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"message": "Notification marked as seen"}), 200

@app.route('/notifications/deactivate', methods=['PUT'])
def deactivate_notifications():
    data = request.json
    flight_id = data.get('flight_id')
    user_id = data.get('user_id')
    
    if not flight_id:
        return jsonify({"error": "Missing flight_id"}), 400
        
    # Deactivate all notifications for this flight except for the booking user
    query = Notification.query.filter_by(flight_id=flight_id, is_active=True)
    
    if user_id:
        query = query.filter(Notification.user_id != user_id)
        
    notifications = query.all()
    
    for notification in notifications:
        notification.is_active = False
        
    db.session.commit()
    
    return jsonify({
        "message": "Notifications deactivated",
        "count": len(notifications)
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5021, debug=True)



