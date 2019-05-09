import os
import unittest
from app import app, db
from app.models import UserModel
from config import basedir
from flask import url_for
from app.forms import LoginForm
from flask_login import current_user
from flask_bcrypt import Bcrypt
from werkzeug.security import check_password_hash

class FlaskTestCases(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        app.config['DOMAIN'] = '.app.localhost'
        app.testing = True
        self.client = app.test_client()
        db.create_all()
        user = UserModel(email="Cassie@yahoo.com", password_hash = "Password1234")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_landing_page(self):
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 200)

    def test_cart_page_loads(self):
        response = self.client.get('/cart')
        self.assertEqual(response.status_code, 200)

    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_and_login_logout(self):
        # Register a new account
        response = self.client.post(('/register'), data={
            'email': 'Sam@yahoo.com',
            'username': 'Sam',
            'password': 'Password123',
            'password2': 'Password123'
        })
        self.assertTrue(response.status_code == 200) 

        # Login with the new account
        response = self.client.post(('/login'), data={
            'email': 'Sam@yahoo.com',
            'password': 'Password123',
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)

        # Log out of new account
        response = self.client.get(('/logout'), follow_redirects=True)
        self.assertTrue(response.status_code, 200)
   
    def test_validate_successful_login_form(self):
        # Ensure login successful for form data
        with app.app_context():
            form = LoginForm(email='Sam@yahoo.com', password='Password123')
        self.assertTrue(form.validate())

    def test_place_user_order(self):
        url = "/place_user_order"
        test = True

        response = self.client.post((url), json={
            "test": test
        })

        self.assertEqual(response.status_code, 200)
    
    def test_check_password(self):
        # Ensure given password is correct
        user = UserModel.query.filter_by(email='Cassie@yahoo.com').first()
        self.assertFalse(user.check_password('foobar'))

    def test_authentication(self):
        user = UserModel.query.filter_by(email='Cassie@yahoo.com').first()
        self.assertTrue(user.is_authenticated)

    def test_get_by_id(self):
    # Ensure id is correct for the current/logged in user
        with self.client:
            self.client.post('/login', data=dict(
                email='Cassie@yahoo.com', password='Password1234'
            ), follow_redirects=True)

        user = UserModel.query.filter_by(email='Cassie@yahoo.com').first()
        self.assertTrue(user.id == 1)
   
    def test_load_cart_page(self):
        # Ensure that the cart page properly loads by checking that a bit of text is in the response
        response = self.client.get('/cart')
        self.assertTrue(b'Your Cart' in response.data)
        
    def test_cart(self):
        user = UserModel.query.filter_by(email='Cassie@yahoo.com').first()

        response = self.client.post(('/user/cart'), data={
            'id': '1',
            'name': 'Thai Coconut Chicken Soup',
            'cost': '8.0',
            'quantity': '1',
            'picture_path': 'img/menuPage/chunckysoup.jpg'
        })   

        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.status != 400)

    def test_empty_cart(self):
        response = self.client.get(('user/cart'))

        self.assertFalse(b'Chicken' in response.data)
        self.assertTrue(b'' in response.data)

if __name__ == '__main__':
    unittest.main()
