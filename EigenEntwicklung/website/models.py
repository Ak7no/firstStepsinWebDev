from . import db #. uses the current package
from flask_login import UserMixin #Special class that helps to create a user table / model 
from sqlalchemy.sql import func #func gets the current timestamp

class Note(db.Model): #Here will be the structure of our note table (columns)
    id = db.Column(db.Integer, primary_key=True) #Primary key is a unique identifier for each record
    data = db.Column(db.String(10000)) #String with max length of 10000 characters
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #DateTime column with timezone, default value is the current timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #Foreign key to link the note to a specific user; Reference to table User and its column id


class User(db.Model, UserMixin): #Here will be the structure of our user table (columns); UserMixin is from Flask-Login module
    id = db.Column(db.Integer, primary_key=True) #Primary key is a unique identifier for each record
    email = db.Column(db.String(150), unique=True) #String with max length of 150 characters, must be unique
    password = db.Column(db.String(150)) #String with max length of 150 characters
    first_name = db.Column(db.String(150)) #String with max length of 150 characters
    notes = db.relationship('Note') #Relationship to link User to their Notes; One-to-many relationship (one user can have many notes), thanks Kirchberg!
   
from datetime import date, datetime
from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy() 

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(100))
    description = db.Column(db.Text)
    price_per_night = db.Column(db.Integer)
    description_long = db.Column(db.Text)
    service_details = db.Column(db.Text)  # New field for hotel services and amenities
    latitude = db.Column(db.Float)
    longtitude = db.Column(db.Float)
    

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    checkin = db.Column(db.Date, nullable=False)
    checkout = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Integer)
    created_at = db.Column(db.Date, default=date.today)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    checkin_date = db.Column(db.Date, nullable=False)      # ← WICHTIG
    checkout_date = db.Column(db.Date, nullable=False)     # ← WICHTIG
    num_guests_adult = db.Column(db.Integer, nullable=False)
    num_guests_child = db.Column(db.Integer)
    special_requests = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    birthdate = db.Column(db.Date)
    guest_number = db.Column(db.Integer)

