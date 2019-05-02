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

    def test_register(self):
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

    def test_check_password(self):
        # Ensure given password is correct
        user = UserModel.query.filter_by(email='Cassie@yahoo.com').first()
        self.assertFalse(user.check_password('foobar'))

    def test_get_by_id(self):
    # Ensure id is correct for the current/logged in user
        with self.client:
            self.client.post('/login', data=dict(
                email='Cassie@yahoo.com', password='Password1234'
            ), follow_redirects=True)

        user = UserModel.query.filter_by(email='Cassie@yahoo.com').first()
        self.assertTrue(user.id == 1)

if __name__ == '__main__':
    unittest.main()
