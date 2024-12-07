from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sarah:sarah@localhost:5433/mysticmenu_db'
db = SQLAlchemy(app)

from app.models import User

def create_admin_user():
    admin_user = User.query.filter_by(id='admin').first()
    if not admin_user:
        # Use bcrypt to hash the password
        password = 'securepassword123'  # Change this to your desired admin password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_admin = User(id='admin', name='Admin User', admin=True, passwd=hashed_password)
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")

with app.app_context():
    db.create_all()
    create_admin_user()