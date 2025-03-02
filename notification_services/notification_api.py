from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId
import logging

# Configure logging
logging.basicConfig(
    filename="notification_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/notification_service"
mongo = PyMongo(app)
notifications = mongo.db.notification  # Collection

# POST: Add a new notification
@app.route("/notifications", methods=["POST"])
def add_notification():
    data = request.json
    logging.info(f"Received POST request: {data}")
    
    if not data or "booking_id" not in data or "user_id" not in data:
        logging.warning("Missing booking_id or user_id in request data")
        return jsonify({"error": "Missing booking_id or user_id"}), 400

    notification_id = notifications.insert_one({
        "booking_id": data["booking_id"],
        "user_id": data["user_id"]
    }).inserted_id
    
    logging.info(f"Notification added with ID: {notification_id}")
    return jsonify({"message": "Notification added", "id": str(notification_id)}), 201

# GET: Retrieve all notifications (or filter by user_id)
@app.route("/notifications/<user_id>", methods=["GET"])
def get_notifications_by_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        logging.error(f"Invalid user_id format: {user_id}")
        return jsonify({"error": "Invalid user_id format"}), 400

    logging.info(f"Fetching notifications for user_id: {user_id}")
    notifications_list = notifications.find({"user_id": user_id})
    
    result = [
        {"booking_id": n["booking_id"], "user_id": n["user_id"]}
        for n in notifications_list
    ]
    
    logging.info(f"Found {len(result)} notifications for user_id {user_id}")
    return jsonify(result), 200

@app.route("/notifications/<user_id>/count", methods=["GET"])
def get_notification_count(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        logging.error(f"Invalid user_id format: {user_id}")
        return jsonify({"error": "Invalid user_id format"}), 400

    count = notifications.count_documents({"user_id": user_id})
    logging.info(f"Notification count for user_id {user_id}: {count}")
    return jsonify({"notification_count": count}), 200

@app.route("/notifications/delete/<booking_id>", methods=["DELETE"])
def delete_notification(booking_id):
    try:
        booking_id = int(booking_id)
    except ValueError:
        logging.error(f"Invalid booking_id format: {booking_id}")
        return jsonify({"error": "Invalid booking_id format"}), 400

    logging.info(f"Attempting to delete notification with booking_id: {booking_id}")
    result = notifications.delete_one({"booking_id": booking_id})

    if result.deleted_count > 0:
        logging.info(f"Notification with booking_id {booking_id} deleted successfully")
        return jsonify({"message": "Notification deleted successfully"}), 200
    else:
        logging.warning(f"Notification with booking_id {booking_id} not found")
        return jsonify({"error": "Notification not found"}), 404

if __name__ == "__main__":
    logging.info("Starting Notification Service on port 5001...")
    app.run(port=5001, debug=True)
