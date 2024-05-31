#__init__.PY
from flask import Flask, request, redirect, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import cx_Oracle
import os
import time
from sqlalchemy import create_engine, text

engine = create_engine('oracle://dsr:dsr@localhost:1521/?service_name=dsrdb')
with engine.connect() as conn:
        select_query = text("SELECT * FROM TLEAVES")
        result = conn.execute(select_query)
        print('results',result,result.first())

db = SQLAlchemy()
DB_NAME = 'database.db'  # This will no longer be used but left for reference

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'DSRAO'
    # Update the SQLALCHEMY_DATABASE_URI to use Oracle
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+cx_oracle://username:password@hostname:port/?service_name=servicename'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://dsr:dsr@localhost:1521/?service_name=dsrdb'

    db.init_app(app)
    # Initialize CSRF protection
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    # The following code is not required for ORACLE as the database is created manually
    # with app.app_context():
    #     create_database()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(emp_code):
      print("load user empcode :",emp_code,type(emp_code))
      with engine.connect() as conn:
        query = text(f"SELECT emp_code, pw, generalname FROM invent.passwords@tams a, empprojtr_master@tams b WHERE a.emp_code=b.id_no AND emp_code = \'{emp_code}\'")
        #query = text(f"SELECT emp_code FROM scott.passwords WHERE emp_code = \'{emp_code}\'")
        print('query ',query)
        result = conn.execute(query).first()
        if result:
            user = User(result[0],result[2])
            print("LOAD_USER :",user)
            return user
        return None

    return app

# THE FOLLOWING FUNCTION IS NOT REQUIRED SINCE THE TABLES ARE CREATED MANUALLY

# def create_database():
#     # Oracle doesn't use path-based databases like SQLite
#     try:
#         db.create_all()
#         print("Database connected and tables created")
#     except Exception as e:
#         print(f"Error creating database: {e}")
