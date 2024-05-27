#models.py
from . import db
from flask_login import UserMixin
from sqlalchemy import func

class User(db.Model, UserMixin):
    __tablename__ = 'users'  # Oracle requires explicit table names with certain length restrictions
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note', backref='user', lazy=True)

class Note(db.Model):
    __tablename__ = 'notes'  # Explicitly define table names
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(4000))
    createdon = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
