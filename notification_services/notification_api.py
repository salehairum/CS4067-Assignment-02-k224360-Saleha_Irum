from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/notification_service"
mongo = PyMongo(app)
notifications = mongo.db.notification  # Collection

# POST: Add a new notification
@app.route("/notifications", methods=["POST"])
def add_notification():
    data = request.json
    if not data or "booking_id" not in data or "user_id" not in data:
        return jsonify({"error": "Missing booking_id or user_id"}), 400

    notification_id = notifications.insert_one({
        "booking_id": data["booking_id"],
        "user_id": data["user_id"]
    }).inserted_id

    return jsonify({"message": "Notification added", "id": str(notification_id)}), 201

# GET: Retrieve all notifications (or filter by user_id)
@app.route("/notifications/<user_id>", methods=["GET"])
def get_notifications_by_user(user_id):
    # Find all notifications for the given user_id
    
    notifications_list = notifications.find({"user_id": user_id})

    # Convert MongoDB documents to JSON format
    result = [
        {"booking_id": n["booking_id"], "user_id": n["user_id"]}
        for n in notifications_list
    ]

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)
