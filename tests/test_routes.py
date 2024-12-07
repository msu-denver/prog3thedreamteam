import pytest
from flask import session
from app import create_app, db
from app.models import User, MysticBurger
import bcrypt
from flask_login import LoginManager

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 'postgresql://sarah:sarah@localhost/test_db',
        "WTF_CSRF_ENABLED": False  # Disable CSRF protection for testing
    })

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_add_to_cart(client, app):
    with app.app_context():
        # Create a test item
        item = MysticBurger(store='Test Store', category='Test Category', item='Test Item', description='Test Description', price=10.0, qty=5, magic=False)
        db.session.add(item)
        db.session.commit()

        # Create and log in as a test user
        user = User(id='testuser', name='Test User', admin=False, passwd=bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()))
        db.session.add(user)
        db.session.commit()
        client.post('/login', data={'id': 'testuser', 'passwd': 'password'}, follow_redirects=True)

        # Add item to cart
        response = client.post(f'/add_to_cart/{item.id}', follow_redirects=True)
        assert response.status_code == 200

        # Trigger a request to commit the session changes
        client.get('/cart')
        
        with client.session_transaction() as sess:
            assert 'cart' in sess
            assert len(sess['cart']) == 1
            assert sess['cart'][0]['id'] == item.id

def test_remove_from_cart(client, app):
    with app.app_context():
        # Create a test item
        item = MysticBurger(store='Test Store', category='Test Category', item='Test Item', description='Test Description', price=10.0, qty=5, magic=False)
        db.session.add(item)
        db.session.commit()

        # Create and log in as a test user
        user = User(id='testuser', name='Test User', admin=False, passwd=bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()))
        db.session.add(user)
        db.session.commit()
        client.post('/login', data={'id': 'testuser', 'passwd': 'password'}, follow_redirects=True)

        # Add item to cart
        client.post(f'/add_to_cart/{item.id}', follow_redirects=True)

        # Trigger a request to commit the session changes
        client.get('/cart')
        
        with client.session_transaction() as sess:
            assert 'cart' in sess
            assert len(sess['cart']) == 1

        # Remove item from cart
        response = client.post(f'/remove_from_cart/{item.id}', follow_redirects=True)
        assert response.status_code == 200

        # Trigger a request to commit the session changes
        client.get('/cart')
        
        with client.session_transaction() as sess:
            assert 'cart' in sess
            assert len(sess['cart']) == 0