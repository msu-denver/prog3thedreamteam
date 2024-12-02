'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s): The Dream Team
Description: Project 3 - Final Project
'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, Optional
from app import db

class User(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    passwd = db.Column(db.LargeBinary, nullable=False)    

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    passwd_confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('passwd', message="Passwords must match")])
    submit = SubmitField('Confirm')

class LoginForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    passwd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class RecipeCreateForm(FlaskForm):
    submit = SubmitField('Confirm')
    
class RecipeUpdateForm(FlaskForm):
    submit = SubmitField('Confirm')

class MenuSearchForm(FlaskForm):
    menu_category = SelectField('Actor Type', choices=[
        ('', 'Any'),
        ('burgers', 'Burgers'), 
        ('desserts', 'Desserts'), 
        ('drinks', 'Drinks'),
        ('sides', 'Sides'),
    ], validators=[Optional()])
    menu_store = SelectField('Store', choices=[
        ('Arcadia Bay', 'arcadia bay'),('Elysium District','elysium district'),
        ('Mystic Falls','mystic falls'),('Neo Tokyo','neo tokyo'),
        ('Cyber City','cyber city')
    ],validators=[Optional()])
    menu_item = StringField('Item', validators=[Optional()])
    menu_magic = SelectField('Magic', choices=[('both', 'Both'), ('true', 'Yes'), ('false', 'No')], validators=[Optional()])
    submit = SubmitField('Search')