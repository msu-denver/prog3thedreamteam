'''
CS3250 - Software Development Methods and Tools - Fall 2024
Instructor: Thyago Mota
Student(s): The Dream Team
Description: Project 2 - Incidents
'''

from flask import Blueprint, render_template
from flask import redirect, url_for, request, session
from flask_login import login_required, login_user, logout_user, current_user
from app import db
from app.models import User, MysticBurger
from app.forms import SignUpForm, LoginForm
from app.forms import RecipeCreateForm, RecipeUpdateForm, MenuSearchForm
import bcrypt

app = Blueprint('main', __name__)


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    categories = [row[0] for row in
                  db.session.query(MysticBurger.category).distinct()]
    stores = [row[0] for row in
              db.session.query(MysticBurger.store).distinct()]

    query = MysticBurger.query
    search = request.args.get('search')
    if search:
        query = query.filter(MysticBurger.item.ilike(f"%{search}%"))

    category = request.args.get('category')
    if category:
        query = query.filter(MysticBurger.category == category)

    store = request.args.get('store')
    if store:
        query = query.filter(MysticBurger.store == store)

    sort_by = request.args.get('sort_by')
    if sort_by:
        query = query.filter(MysticBurger.store == sort_by)

    # pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    recipes = pagination.items

    return render_template('index.html', recipes=recipes,
                           categories=categories,
                           stores=stores,
                           pagination=pagination,
                           sort_by=sort_by)


@app.route('/users/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        if form.passwd.data == form.passwd_confirm.data:
            hashed_passwd = bcrypt.hashpw(
                form.passwd.data.encode('utf-8'), bcrypt.gensalt())
            new_user = User(id=form.id.data, name=form.name.data,
                            admin=False, passwd=hashed_passwd)
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
            print(f"User {user.id} logged in. Admin status: {user.admin}")
            return redirect(url_for('main.index'))
    return render_template('login.html', form=form)


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
            query = query.filter(
                MysticBurger.store.ilike(f"%{form.store.data}%"))
        if form.category.data:
            query = query.filter(
                MysticBurger.category.ilike(f"%{form.category.data}%"))
        if form.item.data:
            query = query.filter(
                MysticBurger.item.ilike(f"%{form.item.data}%"))
        if form.magic.data is not None:
            query = query.filter(MysticBurger.magic == form.magic.data)

    results = query.all()
    return render_template('search.html', form=form, results=results)


@app.route('/recipes/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_recipe(id): # requires admin
    if not current_user.admin:
        return 'Access Denied', 403

    recipe = MysticBurger.query.get_or_404(id)
    form = RecipeUpdateForm(obj=recipe)
    if form.validate_on_submit():
        recipe.category = form.category.data
        recipe.item = form.item.data
        recipe.description = form.description.data
        recipe.price = form.price.data
        recipe.qty_arcadia_bay = form.qty_arcadia_bay.data
        recipe.qty_elysium_district = form.qty_elysium_district.data
        recipe.qty_mystic_falls = form.qty_mystic_falls.data
        recipe.qty_neo_tokyo = form.qty_neo_tokyo.data
        recipe.qty_cyber_city = form.qty_cyber_city.data
        recipe.magic = form.magic.data
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('update_recipe.html', form=form)


@app.route('/recipes/create', methods=['GET', 'POST'])
@login_required
def create_recipe(): # requires admin
    if not current_user.admin:
        return 'Access Denied', 403

    form = RecipeCreateForm()
    if form.validate_on_submit():
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


@app.route('/recipes/delete/<int:id>', methods=['GET', 'POST'])
@app.route('/recipes/delete', methods=['GET', 'POST'])
@login_required
def delete_recipe(id=None): # requires admin
    if not current_user.admin:
        return 'Access Denied', 403

    if request.method == 'POST':
        if id:
            # Single delete
            recipe = MysticBurger.query.get(id)
            if recipe:
                try:
                    db.session.delete(recipe)
                    db.session.commit()
                    db.session.expire_all()
                    print('Recipe successfully deleted.')
                except Exception as e:
                    db.session.rollback()
                    print(f"Error occurred during deletion: {e}")
                    return 'An error occurred while deleting the recipe.', 500
            else:
                print('Recipe not found.')
        else:
            # Multiple delete
            item_ids = request.form.getlist('item_ids')
            if item_ids:
                try:
                    for item_id in item_ids:
                        recipe = MysticBurger.query.get(item_id)
                        if recipe:
                            db.session.delete(recipe)
                    db.session.commit()
                    db.session.expire_all()
                    print('Recipes successfully deleted.')
                except Exception as e:
                    db.session.rollback()
                    print(f"Error occurred during deletion: {e}")
                    return 'An error occurred while deleting the recipes.', 500

    form = MenuSearchForm()
    page = request.args.get('page', 1, type=int)
    pagination = MysticBurger.query.paginate(page=page, per_page=10)
    return render_template('delete_recipe.html', form=form,
                           recipes=pagination.items,
                           pagination=pagination,
                           current_page=page,
                           total_pages=pagination.pages)


@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', [])
    total = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)


@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
@login_required
def add_to_cart(item_id):
    item = MysticBurger.query.get(item_id)
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(
        {'id': item.id, 'name': item.item, 'price': item.price})
    session.modified = True
    return redirect(url_for('main.index'))


@app.route('/remove_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != item_id]
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('main.cart'))
