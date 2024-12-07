'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s): The Dream Team
Description: Project 3 - Final Project
'''
from flask import Flask
from flask_login import LoginManager
from app.extensions import db
from app.models import User
import os

def create_app():
    app = Flask('Menu Web App')
    app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://sarah:sarah@localhost:5433/mysticmenu_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes import app as main_bp
    app.register_blueprint(main_bp)

    @app.cli.command('init-db')
    def init_db():
        with app.app_context():
            db.create_all()
            print("Database initialized!")

    @app.cli.command('load-data')
    def load_data_command():
        from load_data import load_data
        load_data()

    return app

app = create_app()

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)