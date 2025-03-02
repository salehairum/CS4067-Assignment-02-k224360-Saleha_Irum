#running on http://127.0.0.1:5000

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app, origins=["http://127.0.0.1:5500"])

# Configure PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devops:devops24@localhost:5432/booking_service'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Booking model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables before the first request
with app.app_context():
    db.create_all()

# Route to create a new booking
@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    
    event_id = data['event_id']
    requested_tickets = data['ticket_count']  # New field

    # Step 1: Check and Reserve Tickets in Event API
    event_api_url = f"http://localhost:8080/api/events/{event_id}/reserve-tickets"
    response = requests.post(event_api_url, json={"requestedTickets": requested_tickets})

    if response.status_code != 200 or not response.json():  
        return jsonify({"error": "Not enough tickets available"}), 400

    # Step 2: Proceed with Booking
    new_booking = Booking(user_id=data['user_id'], event_id=event_id)
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({"message": "Booking created", "booking_id": new_booking.id}), 201

# Route to get all bookings
@app.route('/bookings', methods=['GET'])
def get_all_bookings():
    bookings = Booking.query.all()
    all_bookings = [
        {
            "id": booking.id,
            "user_id": booking.user_id,
            "event_id": booking.event_id,
            "status": booking.status,
            "created_at": booking.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for booking in bookings
    ]
    
    return jsonify(all_bookings), 200

# Route to get all bookings for a specific user
@app.route('/bookings/user/<int:user_id>', methods=['GET'])
def get_bookings_by_user(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).all()

    if not bookings:
        return jsonify({"message": "No bookings found for this user"}), 404

    user_bookings = [
        {
            "id": booking.id,
            "user_id": booking.user_id,
            "event_id": booking.event_id,
            "status": booking.status,
            "created_at": booking.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for booking in bookings
    ]

    return jsonify(user_bookings), 200

if __name__ == '__main__':
    app.run(debug=True) 
