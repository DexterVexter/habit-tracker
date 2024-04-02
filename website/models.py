from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Boolean
from sqlalchemy import Date

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())


    habits = db.relationship('Habit', backref='user', lazy=True)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    consecutive_days = db.Column(db.Integer, default=0)
    completed = db.Column(Boolean, default=False)
    day_of_fulfillment = db.Column(Date)


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
