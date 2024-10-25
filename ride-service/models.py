from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ride(db.Model):
    __tablename__ = 'rides'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    pickup_location = db.Column(db.String(255), nullable=False)
    dropoff_location = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
