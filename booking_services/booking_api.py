import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import requests
import pika
import json
from flask_restx import Api, Resource, fields

# Configure logging
logging.basicConfig(
    filename="booking_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("BookingService")

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])

# Configure PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devops:devops24@localhost:5432/booking_service'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app, version='1.0', title='Booking API', description='API for managing event bookings')

ns = api.namespace('bookings', description='Booking operations')

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

# Swagger models
booking_model = api.model('Booking', {
    'user_id': fields.Integer(required=True, description='User ID'),
    'event_id': fields.Integer(required=True, description='Event ID'),
    'status': fields.String(default='pending', description='Booking status')
})

@ns.route('/')
class BookingList(Resource):
    @api.doc('list_bookings')
    def get(self):
        """Get all bookings"""
        logger.info("Fetching all bookings")
        bookings = Booking.query.all()
        return [{
            "id": booking.id,
            "user_id": booking.user_id,
            "event_id": booking.event_id,
            "status": booking.status,
            "created_at": booking.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for booking in bookings], 200

    @api.expect(booking_model)
    @api.doc('create_booking')
    def post(self):
        """Create a new booking"""
        data = request.get_json()
        new_booking = Booking(user_id=data['user_id'], event_id=data['event_id'])
        db.session.add(new_booking)
        db.session.commit()
        return {"message": "Booking created", "booking_id": new_booking.id}, 201

@ns.route('/user/<int:user_id>')
@api.doc(params={'user_id': 'User ID'})
class UserBookings(Resource):
    def get(self, user_id):
        """Get all bookings for a specific user"""
        logger.info(f"Fetching bookings for user {user_id}")
        bookings = Booking.query.filter_by(user_id=user_id).all()
        if not bookings:
            return {"message": "No bookings found for this user"}, 404
        return [{
            "id": booking.id,
            "user_id": booking.user_id,
            "event_id": booking.event_id,
            "status": booking.status,
            "created_at": booking.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for booking in bookings], 200

@ns.route('/<int:booking_id>/status')
@api.doc(params={'booking_id': 'Booking ID'})
class BookingStatus(Resource):
    @api.expect(api.model('BookingStatus', {
        'status': fields.String(required=True, description='New booking status')
    }))
    def patch(self, booking_id):
        """Update booking status"""
        data = request.get_json()
        booking = Booking.query.get(booking_id)
        if not booking:
            return {"error": "Booking not found"}, 404
        booking.status = data["status"]
        db.session.commit()
        return {"message": "Booking status updated successfully"}, 200

api.add_namespace(ns, path='/bookings')

if __name__ == '__main__':
    app.run(debug=True)
