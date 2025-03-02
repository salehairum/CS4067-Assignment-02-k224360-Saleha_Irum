from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId
import logging
from flask_restx import Api, Resource, fields

# Configure logging
logging.basicConfig(
    filename="notification_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])
api = Api(app, title="Notification Service API", description="API for managing notifications", doc="/")

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/notification_service"
mongo = PyMongo(app)
notifications = mongo.db.notification  # Collection

# Swagger Models
notification_model = api.model("Notification", {
    "booking_id": fields.Integer(required=True, description="Booking ID"),
    "user_id": fields.Integer(required=True, description="User ID")
})

@api.route("/notifications")
class NotificationResource(Resource):
    @api.expect(notification_model)
    @api.response(201, "Notification added")
    @api.response(400, "Missing booking_id or user_id")
    def post(self):
        """Add a new notification"""
        data = request.json
        logging.info(f"Received POST request: {data}")
        
        if not data or "booking_id" not in data or "user_id" not in data:
            logging.warning("Missing booking_id or user_id in request data")
            return {"error": "Missing booking_id or user_id"}, 400

        notification_id = notifications.insert_one({
            "booking_id": data["booking_id"],
            "user_id": data["user_id"]
        }).inserted_id
        
        logging.info(f"Notification added with ID: {notification_id}")
        return {"message": "Notification added", "id": str(notification_id)}, 201

@api.route("/notifications/<int:user_id>")
class UserNotifications(Resource):
    @api.response(200, "Success")
    @api.response(400, "Invalid user_id format")
    def get(self, user_id):
        """Retrieve notifications for a specific user"""
        logging.info(f"Fetching notifications for user_id: {user_id}")
        notifications_list = notifications.find({"user_id": user_id})
        
        result = [
            {"booking_id": n["booking_id"], "user_id": n["user_id"]}
            for n in notifications_list
        ]
        
        logging.info(f"Found {len(result)} notifications for user_id {user_id}")
        return result, 200

@api.route("/notifications/<int:user_id>/count")
class NotificationCount(Resource):
    @api.response(200, "Success")
    @api.response(400, "Invalid user_id format")
    def get(self, user_id):
        """Retrieve the count of notifications for a specific user"""
        count = notifications.count_documents({"user_id": user_id})
        logging.info(f"Notification count for user_id {user_id}: {count}")
        return {"notification_count": count}, 200

@api.route("/notifications/delete/<int:booking_id>")
class DeleteNotification(Resource):
    @api.response(200, "Notification deleted successfully")
    @api.response(404, "Notification not found")
    @api.response(400, "Invalid booking_id format")
    def delete(self, booking_id):
        """Delete a notification by booking_id"""
        logging.info(f"Attempting to delete notification with booking_id: {booking_id}")
        result = notifications.delete_one({"booking_id": booking_id})

        if result.deleted_count > 0:
            logging.info(f"Notification with booking_id {booking_id} deleted successfully")
            return {"message": "Notification deleted successfully"}, 200
        else:
            logging.warning(f"Notification with booking_id {booking_id} not found")
            return {"error": "Notification not found"}, 404

if __name__ == "__main__":
    logging.info("Starting Notification Service on port 5001...")
    app.run(port=5001, debug=True)
