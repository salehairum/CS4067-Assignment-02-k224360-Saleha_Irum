from database import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'booking'  # Explicitly setting the table name

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Booking {self.id}, User {self.user_id}, Event {self.event_id}, Status {self.status}>"
