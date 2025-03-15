import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import requests
import pika
import json
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    filename="booking_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("BookingService")

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["http://localhost:5500", "http://frontend:5500"])

# Configure PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
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
    requested_tickets = data['ticket_count']

    logger.info(f"Received booking request for event {event_id} by user {data['user_id']}")

    # Step 1: Check and Reserve Tickets in Event API
    event_api_url = f"http://event_service:8080/api/events/{event_id}/reserve-tickets"
    response = requests.post(event_api_url, json={"requestedTickets": requested_tickets})

    if response.status_code != 200 or not response.json():
        logger.warning(f"Ticket reservation failed for event {event_id}")
        return jsonify({"error": "Not enough tickets available"}), 400

    logger.info(f"Successfully reserved {requested_tickets} tickets for event {event_id}")

    # Step 2: Verify Payment
    payment_api_url = "http://payment_service:5002/verify-payment"
    payment_response = requests.post(payment_api_url, json={"user_id": data['user_id'], "amount": data.get("price", 0)})

    if payment_response.status_code != 200:
        logger.warning(f"Payment verification failed for user {data['user_id']}")
        return jsonify({"error": "Payment failed"}), 400

    logger.info(f"Payment successful for user {data['user_id']}")

    # Step 3: Proceed with Booking
    new_booking = Booking(user_id=data['user_id'], event_id=event_id)
    db.session.add(new_booking)
    db.session.commit()

    logger.info(f"Booking created with ID {new_booking.id} for user {data['user_id']}")

    publish_notification(data['user_id'], new_booking.id)

    return jsonify({"message": "Booking created", "booking_id": new_booking.id}), 201

# Route to get all bookings
@app.route('/bookings', methods=['GET'])
def get_all_bookings():
    logger.info("Fetching all bookings")
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
    logger.debug(f"Total bookings fetched: {len(all_bookings)}")
    return jsonify(all_bookings), 200

# Route to get all bookings for a specific user
@app.route('/bookings/user/<int:user_id>', methods=['GET'])
def get_bookings_by_user(user_id):
    logger.info(f"Fetching bookings for user {user_id}")
    bookings = Booking.query.filter_by(user_id=user_id).all()

    if not bookings:
        logger.warning(f"No bookings found for user {user_id}")
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

    logger.debug(f"User {user_id} has {len(user_bookings)} bookings")
    return jsonify(user_bookings), 200

# Route to update the status of a booking
@app.route('/bookings/<int:booking_id>/status', methods=['PATCH'])
def update_booking_status(booking_id):
    data = request.get_json()

    if not data or "status" not in data:
        logger.warning("Invalid booking status update request")
        return jsonify({"error": "Missing 'status' field"}), 400

    booking = Booking.query.get(booking_id)

    if not booking:
        logger.warning(f"Booking ID {booking_id} not found for status update")
        return jsonify({"error": "Booking not found"}), 404

    booking.status = data["status"]
    db.session.commit()

    logger.info(f"Updated booking {booking_id} status to {data['status']}")
    return jsonify({"message": "Booking status updated successfully"}), 200

def publish_notification(user_id, booking_id):
    try:
        rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
        rabbitmq_port = int(os.getenv("RABBITMQ_PORT", 5672))

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port))
        channel = connection.channel()
        channel.queue_declare(queue='notifications')

        message = json.dumps({"user_id": user_id, "booking_id": booking_id})
        channel.basic_publish(exchange='', routing_key='notifications', body=message)

        connection.close()
        logger.info(f"Notification sent for booking {booking_id} to user {user_id}")

    except Exception as e:
        logger.error(f"Failed to send notification for booking {booking_id}: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
