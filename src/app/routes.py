'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s):
Description: Project 2 - Incidents
'''

from flask import Blueprint, render_template, redirect, url_for, request, session
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
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = MysticBurger.query.paginate(page=page, per_page=per_page, error_out=False)
    recipes = pagination.items
    return render_template('index.html', recipes=recipes, pagination=pagination)

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
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = MysticBurger.query.paginate(page=page, per_page=per_page, error_out=False)
    recipes = pagination.items
    stores = ['Arcadia Bay', 'Elysium District', 'Mystic Falls', 'Neo Tokyo', 'Cyber City']
    sort_by = request.args.get('sort_by', 'Arcadia Bay')
    return render_template('index.html', recipes=recipes, pagination=pagination, stores=stores, sort_by=sort_by)

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

@app.route('/admin_dashboard/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_recipe(id): # requires admin
    form = RecipeUpdateForm()
    if form.validate_on_submit():
        if current_user.is_admin:
            stores = [
            ('Arcadia Bay', form.qty_arcadia_bay.data),
            ('Elysium District', form.qty_elysium_district.data),
            ('Mystic Falls', form.qty_mystic_falls.data),
            ('Neo Tokyo', form.qty_neo_tokyo.data),
            ('Cyber City', form.qty_cyber_city.data)
        ]
        for store, qty in stores:
            new_recipe = MysticBurger(
                category=form.category.data,
                store=store,
                item=form.item.data,
                description=form.description.data,
                price=form.price.data,
                qty=qty,
                magic=form.magic.data
            )
            db.session.add(new_recipe)
        
        db.session.commit()
        print('Recipe added successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_recipe.html', form=form)

@app.route('/admin_dashboard/create', methods=['GET', 'POST'])
@login_required
def create_recipe(): # requires admin
    form = RecipeCreateForm()
    if form.validate_on_submit():
        if current_user.is_admin:
            stores = [
            ('Arcadia Bay', form.qty_arcadia_bay.data),
            ('Elysium District', form.qty_elysium_district.data),
            ('Mystic Falls', form.qty_mystic_falls.data),
            ('Neo Tokyo', form.qty_neo_tokyo.data),
            ('Cyber City', form.qty_cyber_city.data)
            ]
            for store, qty in stores:
                new_recipe = MysticBurger(
                    category=form.category.data,
                    store=store,
                    item=form.item.data,
                    description=form.description.data,
                    price=form.price.data,
                    qty=qty,
                    magic=form.magic.data
            )
            db.session.add(new_recipe)
            
            db.session.commit()
            print('Recipe added successfully!', 'success')
            return redirect(url_for('main.index'))
        return render_template('create_recipe.html', form=form)
    

@app.route('/admin_dashboard/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_recipe(id): # requires admin
    if current_user.is_admin:
        recipe = MysticBurger.query.get(id)
        if recipe:
            try:
                db.session.delete(recipe)
                db.session.commit()
                db.session.expire_all()
                print('recipe successfully deleted.')
            except Exception as e:
                db.session.rollback()
                print(f"Error occurred during deletion: {e}")
                return 'An error occurred while deleting the incident.', 500
        else:
            print('Incident not found.')
        # Refresh the incident list with pagination after deletion
        form = MenuSearchForm()
        page = request.args.get('page', 1, type=int)
        pagination = MysticBurger.query.paginate(page=page, per_page=10)
        return render_template('index.html', form=form, incidents=pagination.items,
                               pagination=pagination, current_page=page, total_pages=pagination.pages)
    else:
        return 'User does not have credentials...Access Denied', 403
    
@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    item = MysticBurger.query.get(item_id)
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append({'id': item.id, 'name': item.item, 'price': item.price})
    session.modified = True
    return redirect(url_for('main.index'))

@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != item_id]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('main.cart'))



#Testing function:
#@app.route('/populate-db')
#def populate_db():
#   sample_burgers = [
#        MysticBurger(store='Mystic Store 1', category='Burgers', item='Mystic Burger', description='A magical burger', price=9.99, qty=10, magic=True),
#        MysticBurger(store='Mystic Store 2', category='Drinks', item='Mystic Shake', description='A magical shake', price=4.99, qty=20, magic=True),
#        MysticBurger(store='Mystic Store 3', category='Sides', item='Mystic Fries', description='Magical fries', price=2.99, qty=30, magic=False)
#    ]
#    db.session.bulk_save_objects(sample_burgers)
#    db.session.commit()
#    return "Database populated."