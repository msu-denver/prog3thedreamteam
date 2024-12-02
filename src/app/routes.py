'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s):
Description: Project 2 - Incidents
'''

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from app import db
from app.models import User, Recipe, MysticBurger
from app.forms import SignUpForm, LoginForm, RecipeCreateForm, RecipeUpdateForm, MenuSearchForm
import bcrypt

# Define the blueprint
app = Blueprint('main', __name__)

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 
    recipes = MysticBurger.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.passwd.data == form.passwd_confirm.data:
            hashed_passwd = bcrypt.hashpw(form.passwd.data.encode('utf-8'), bcrypt.gensalt())
            new_user = User(id=form.id.data, name=form.name.data, admin=False, passwd=hashed_passwd)
            existing_user = User.query.filter_by(id=form.id.data).first()
            if existing_user:
                return ('User already exists')            
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('main.index'))
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user and bcrypt.checkpw(form.passwd.data.encode(), user.passwd):
            login_user(user)
            return redirect(url_for('main.dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    recipes = MysticBurger.query.all()  # Query all recipes
    return render_template('index.html', recipes=recipes)

@app.route('/users/signout', methods=['GET', 'POST'])
@login_required
def signout():
    logout_user()
    return redirect(url_for('main.index'))

@app.route('/recipes/search', methods=['GET', 'POST'])
def search_menu():
    form = MenuSearchForm()
    query = MysticBurger.query

    if form.validate_on_submit():
        if form.store.data:
            query = query.filter(MysticBurger.store.ilike(f"%{form.store.data}%"))
        if form.category.data:
            query = query.filter(MysticBurger.category.ilike(f"%{form.category.data}%"))
        if form.item.data:
            query = query.filter(MysticBurger.item.ilike(f"%{form.item.data}%"))
        if form.magic.data is not None:
            query = query.filter(MysticBurger.magic == form.magic.data)

    results = query.all()
    return render_template('search.html', form=form, results=results)

@app.route('/incidents', methods=['GET'])
def list_recipes():
    return 'Work in progress...'

@app.route('/incidents/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_recipe(id): # requires admin
    form = RecipeUpdateForm()
    if form.validate_on_submit():
        # Add your update logic here
        pass
    return render_template('update_recipe.html', form=form)

@app.route('/incidents/create', methods=['GET', 'POST'])
@login_required
def create_recipe(): # requires admin
    form = RecipeCreateForm()
    if form.validate_on_submit():
        # Add your create logic here
        pass
    return render_template('create_recipe.html', form=form)

@app.route('/populate-db')
def populate_db():
    sample_burgers = [
        MysticBurger(store='Mystic Store 1', category='Burgers', item='Mystic Burger', description='A magical burger', price=9.99, qty=10, magic=True),
        MysticBurger(store='Mystic Store 2', category='Drinks', item='Mystic Shake', description='A magical shake', price=4.99, qty=20, magic=True),
        MysticBurger(store='Mystic Store 3', category='Sides', item='Mystic Fries', description='Magical fries', price=2.99, qty=30, magic=False)
    ]
    db.session.bulk_save_objects(sample_burgers)
    db.session.commit()
    return "Database populated with sample data!"