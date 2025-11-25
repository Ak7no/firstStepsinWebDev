from . import db #. uses the current package
from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100))
    description = db.Column(db.Text)
    price_per_night = db.Column(db.Integer)
    price_per_night_u1 = db.Column(db.Integer)
    price_per_night_u2 = db.Column(db.Integer)
    price_per_night_u3 = db.Column(db.Integer)
    description_long = db.Column(db.Text)
    service_details = db.Column(db.Text)  
    latitude = db.Column(db.Float)
    longtitude = db.Column(db.Float)
    hotel_email = db.Column(db.String(150))
    hotel_phone = db.Column(db.String(50))
    hotel_website = db.Column(db.String(200))
    hotel_street = db.Column(db.String(200))

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    birthdate = db.Column(db.Date)
    guest_number = db.Column(db.Integer)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guest_id =db.Column(db.Integer, db.ForeignKey('guest.id'))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    checkin_date = db.Column(db.Date, nullable=False)    
    checkout_date = db.Column(db.Date, nullable=False)  
    num_guests_adult = db.Column(db.Integer, nullable=False)
    num_guests_child = db.Column(db.Integer)
    special_requests = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Integer)
    creditcard_name = db.Column(db.String(100))
    creditcard_number = db.Column(db.String(20))
    creditcard_expiry = db.Column(db.String(7)) 
    creditcard_cvc = db.Column(db.String(4))

