import os
import unittest
from app import app, db
from app.models import UserModel
from config import basedir
from flask import url_for

class FlaskTestCases(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        #app.config['SERVER_NAME'] = 'localhost'
        app.config['DOMAIN'] = '.app.localhost'
        app.testing = True
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_page(self):
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 200)
        #self.assertTrue(b'Stranger' in response.data)

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
        #response = self.client.get(('/logout'), follow_redirects=True)
        #self.assertTrue(b'You have been logged out' in response.data)
    
    def test_add_to_cart(self):
        # Get next item id
        next_item_id = self.client.get("/items/get_next_id")

        # Post item to cart
        response = self.client.post(('/user/cart'), data={
            name: "Thai Coconut Chicken Soup", 
            quantity: 2, 
            id = next_item_id, 
            cost: 8
        })

        self.assertEqual(response.status_code, 200)



    
if __name__ == '__main__':
    unittest.main()