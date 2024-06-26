#models.py
from . import db, engine
from flask_login import UserMixin, current_user
from sqlalchemy import func
from pydantic import BaseModel,Field
from sqlalchemy import text

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

class Leavebal(BaseModel):
    cl_bal: float
    el_bal: float
    sl_bal: float
    ot_bal: float

    @classmethod
    def get_leave_balance(cls, emp_code):
        print("Fetching leave balance for:", emp_code)
        with engine.connect() as conn:
            query = f"select CLSBAL, ELSBAL, SLSBAL, OHSBAL from OPBAL@tams where actinact=1 and id_no='{emp_code}'"
            select_query = text(query)
            result = conn.execute(select_query).fetchone()
            if result:
                return cls(
                    cl_bal=float(result[0]),
                    el_bal=float(result[1]),
                    sl_bal=float(result[2]),
                    ot_bal=float(result[3])
                )
            else:
                raise ValueError("No data found for the given employee code")
            