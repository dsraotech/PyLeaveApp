from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os

db = SQLAlchemy()
DB_NAME='database.db'


def Create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='DSRAO'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views1  # Reads the views.py and find the object views1
    from .auth import auth

    app.register_blueprint(views1,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User, Note
    with app.app_context():
        create_database(app)

    return app

def create_database(app):
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(BASE_DIR, DB_NAME)
    print(db_path)
    print('Check if database exist')
#    if not path.exists('website/'+DB_NAME):
    if not path.exists(db_path):
        db.create_all()
        print("Database created")
    else:
        print("Database already exists")