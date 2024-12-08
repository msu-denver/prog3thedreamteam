from app.models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://sarah:sarah@localhost:5433/mysticmenu_db'
db = SQLAlchemy(app)

# hardcodes admin user ID:admin PW:admin

def create_admin_user():
    admin_user = User.query.filter_by(id='admin').first()
    if not admin_user:
        password = 'admin'
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        new_admin = User(id='admin', name='Admin User',
                         admin=True, passwd=hashed_password)
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print("Admin user already exists.")


with app.app_context():
    db.create_all()
    create_admin_user()
