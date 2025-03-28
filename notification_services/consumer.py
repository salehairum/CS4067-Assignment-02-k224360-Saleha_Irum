import pika
import json
from pymongo import MongoClient
import os
import logging

logging.basicConfig(
    filename="notification_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Connect to MongoDB
client = MongoClient("mongodb://mongodb:27017/")
db = client["notification_service"]
notifications = db["notification"]

# Connect to RabbitMQ
rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
rabbitmq_port = int(os.getenv("RABBITMQ_PORT", 5672))
rabbitmq_user = os.getenv("RABBITMQ_DEFAULT_USER", "guest")  
rabbitmq_pass = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")

# Set credentials for authentication
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)

# Connect to RabbitMQ with authentication
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
)
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
    logging.info(f"Received notification: User {user_id}, Booking {booking_id}")

# Set up consumer
channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)

print("Waiting for messages. To exit, press CTRL+C")
logging.info(f"Waiting for messages.")
channel.start_consuming()
