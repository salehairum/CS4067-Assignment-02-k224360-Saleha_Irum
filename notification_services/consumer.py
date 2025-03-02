import pika
import json
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["notification_service"]
notifications = db["notification"]

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='notifications')

# Define a callback function that runs when a message is received
def callback(ch, method, properties, body):
    data = json.loads(body)
    user_id = data["user_id"]
    booking_id = data["booking_id"]

    # Store notification in MongoDB
    notifications.insert_one({"user_id": user_id, "booking_id": booking_id})

    print(f"Received notification: User {user_id}, Booking {booking_id}")

# Set up consumer
channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)

print("Waiting for messages. To exit, press CTRL+C")
channel.start_consuming()
