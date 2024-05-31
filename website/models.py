#models.py
from . import db
from flask_login import UserMixin
from sqlalchemy import func

class User(UserMixin):
    def __init__(self, emp_code,emp_name):
        self.emp_code = emp_code
        self.emp_name = emp_name
    
    @property
    def id(self):
        return self.emp_code
   
class Note(db.Model):
    __tablename__ = 'notes'  # Explicitly define table names
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(4000))
    createdon = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    
