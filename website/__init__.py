#__init__.PY
from flask import Flask, request, redirect, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import cx_Oracle
import os
import time

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
    def load_user(id):
        return User.query.get(int(id))

    return app

# THE FOLLOWING FUNCTION IS NOT REQUIRED SINCE THE TABLES ARE CREATED MANUALLY

# def create_database():
#     # Oracle doesn't use path-based databases like SQLite
#     try:
#         db.create_all()
#         print("Database connected and tables created")
#     except Exception as e:
#         print(f"Error creating database: {e}")
