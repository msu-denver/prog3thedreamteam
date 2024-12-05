'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s): The Dream Team
Description: Project 3 - Final Project
'''

from flask_login import UserMixin
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    about = db.Column(db.String(256))
    admin = db.Column(db.Boolean, default=False)
    passwd = db.Column(db.LargeBinary, nullable=False)

    def set_password(self, password):
        self.passwd = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwd, password)

    def __str__(self):
        return f'{self.id}, {self.name}'

class RecipeType(db.Model):
    __tablename__ = 'recipe_types'
    code = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(256), nullable=False)

    def __str__(self):
        return f'{self.code}, {self.description}'

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)  # Added primary key
    name = db.Column(db.String(256), nullable=False)
    recipe_type_code = db.Column(db.Integer, db.ForeignKey('recipe_types.code'))
    recipe_type = db.relationship('RecipeType', foreign_keys=[recipe_type_code])
    description = db.Column(db.String(256), nullable=False)
    magic = db.Column(db.Boolean, nullable=False)

class MysticBurger(db.Model):
    __tablename__ = 'mysticburgers'
    __table_args__ = {'schema': 'public'}  # Specify the schema explicitly


    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String(64))
    category = db.Column(db.String(64))
    item = db.Column(db.String(64))
    description = db.Column(db.String(256))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    magic = db.Column(db.Boolean)

    def __str__(self):
        return f'{self.store}, {self.category}, {self.item}, {self.description}, {self.price}, {self.qty}, {self.magic}'