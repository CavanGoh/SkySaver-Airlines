from flask import Flask
from compositeMicroservices.BookingManagement import booking_management
# Import other blueprints as needed

app = Flask(__name__)
app.register_blueprint(booking_management)
# Register other blueprints

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
