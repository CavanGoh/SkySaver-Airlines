from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
CORS(app, supports_credentials=True) 

# Configure session
app.secret_key = 'iloveesd' 
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Database config
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/user'

from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

db_base = os.getenv("hostdbURL")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    # db_base + "/user"
    # if db_base else 
    "mysql+mysqlconnector://root@host.docker.internal:3306/user"
)#checks in the ".env" file for "dbURL"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120))
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name
        }

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name', '')
    
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 409
    
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, name=name)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"message": f"Registration failed: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid credentials"}), 401
    

    session['user_id'] = user.id
    
    return jsonify({
        "message": "Login successful",
        "user": user.to_dict()
    }), 200

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        return jsonify({"message": "Not logged in"}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return jsonify({"message": "User not found"}), 404
    
    return jsonify({"user": user.to_dict()}), 200

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "User service is running"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='test@gmail.com').first():
            test_user = User(
                email='test@gmail.com',
                password=generate_password_hash('test'),
                name='Test User'
            )
            db.session.add(test_user)
            db.session.commit()
            print("Test user created with email 'test' and password 'test'")
    app.run(host='0.0.0.0', port=5500, debug=True)