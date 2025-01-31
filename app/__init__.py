from flask import Flask, redirect, url_for, session
from flask_session import Session
from pymongo import MongoClient
import os

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))  
    
   
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    
    client = MongoClient('localhost', 27017)
    app.db = client['Test_Generator']


    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='')
    from app.routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp)
    from app.routes.student_routes import student_bp
    app.register_blueprint(student_bp)


    try:
        app.db.list_collection_names() 
        print("Connected to MongoDB successfully!")
    except Exception as e:
        print("Failed to connect to MongoDB:", e)

    return app