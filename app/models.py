from app import db
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


"""
Admin Model

@Parameters
    id - The id of the admin
    name - The name of the admin
    orders - This will be a list of ALL ORDERS 
                -Orders will contain a completed boolean value that 
                will be used to see if the admin needs to have order delivered
                
    Admin should NOT be deletable
    
    The admin will be able to add and delete food items as-well-as ingredients.
    The admin will be able to see a list of all orders, active orders, and completed orders
"""


class AdminModel(db.Model):

    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)

    orders = db.relationship('OrderModel', backref='admin_in_charge')



    def __repr__(self):
        return '<Admin {}>'.format(self.name)


"""
User Model

@Parameters
    id - The id of the User
    first_name - users first name
    .
    .
    phone_number - user phone numbers
    
    orders - a list of all the users orders, if the orders boolean variable completed is false, then 
    this is the users current order
    
    temp users will only have one order on their list and the one order completed should be false
"""

class UserModel(UserMixin, db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    first_name = db.Column(db.String(64), index=True, unique=False)
    last_name = db.Column(db.String(64), index=True, unique=False)
    address_line_1 = db.Column(db.String(64), index=True, unique=False)
    address_line_2 = db.Column(db.String(64), index=True, unique=False)
    city = db.Column(db.String(64), index=True, unique=False)
    state = db.Column(db.String(64), index=True, unique=False)
    zip_code = db.Column(db.String(64), index=True, unique=False)
    phone_number = db.Column(db.String(64), index=True, unique=False)
    image_file = db.Column(db.String(20), index=True, unique=False, nullable=False, default='default.jpg')

    orders = db.relationship('OrderModel', backref='previous_orders')
    items = db.relationship('ItemModel', backref='my_items')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

"""
class UserModel(db.Model):

    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(64), index=True, unique=False)
    first_name = db.Column(db.String(64), index=True, unique=False)
    last_name = db.Column(db.String(64), index=True, unique=False)
    address1 = db.Column(db.String(64), index=True, unique=False)
    address2 = db.Column(db.String(64), index=True, unique=False)
    state = db.Column(db.String(64), index=True, unique=False)
    zip = db.Column(db.String(64), index=True, unique=False)
    phone_number = db.Column(db.String(64), index=True, unique=False)

    orders = db.relationship('OrderModel', backref='related_orders')

    system_controller_id = db.Column(db.Integer, db.ForeignKey('system.id'))


    def __repr__(self):
        return '<User {}>'.format(self.name)
"""

"""
Order Model (Cart Model)

Order is empty and contains no items until user presses add to cart

@Parameters
    id - id number of that order, ever order ever created will have a new number, if a person enters
         the website and no order is made, the temp user will be deleted along with the order
    order_items - all items listed in the order
    cost - sum of all the costs in order_items
    completed - a variable to tell, for users, if the order is their current order, or, for admins,
                is a variable to tell them if the order needs to be delivered
    user_id - the user the order belongs to
    admin_id - admin id should always be 0, which will be Scott's id
    
If an order is made, completed variable becomes false and a new order object is created with 
completed variable true
"""


class OrderModel(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float)
    completed = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

    order_items = db.relationship('ItemModel', backref='order_items')

    def __repr__(self):
        return '<Order {}>'.format(self.name)


"""
Item Model

An item object is created when a gift card, food, or a package is added to a cart, 
it becomes an 'item'and 'item' will inherent the qualities of the food, package, 
or gift card it has in common and will also gain a 

@Parameters
    id - item id
    name - name of the item, food will be the name of the food, 
           for gift card name will be Gift Card, for package it will be 
           3-Package or 5-Package
    cost - cost of food item, gift card or package
    order_id - order id that the item is becoming attached to
    type - food for food, package for package, gc for gift card
    picture - this icon or picture of the item
           
           
Items will only be created once food, a package, or a gift card is added to an order
(An item will be added to the order, not the food, package, or gift card)

When a user creates an item, the order id that is created when the user enters the website
will be used to determine where the item goes
"""


class ItemModel(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    cost = db.Column(db.Float, unique=False)
    # order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    # type = db.Column(db.String(64), index=True, unique=False)
    picture_path = db.Column(db.String(64), index=True, unique=False)
    quantity = db.Column(db.Integer, index=True, unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.name)


"""
Package Model

A package will only be created when a user goes to the package page, once the package is created, a user 
will choose the food items they want to go in the package, if the user cancels the creation, the package is deleted.
If the user creates the package, it becomes an item, and gets added to an order, then it is deleted.

@Parameters
    id - id of the package
    package_type - type of package, used to determine how many food items will be added
    cost - the sum of all the food item costs
"""
class PackageModel(db.Model):
    __tablename__ = "package"

    id = db.Column(db.Integer, primary_key=True)
    package_type = db.Column(db.String(64), index=True, unique=False)
    cost = db.Column(db.Float, primary_key=True)
    food_item_one_id = db.Column(db.Integer, primary_key=True)
    food_item_two_id = db.Column(db.Integer, primary_key=True)
    food_item_three_id = db.Column(db.Integer, primary_key=True)
    food_item_four_id = db.Column(db.Integer, primary_key=True)
    food_item_five_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Package {}>'.format(self.name)


"""
Food Model

Food objects are only created when an admin adds a food item to the database.
There should be no need to "adjust" a food item. Only either add a new one entirely or delete one.

@parameters
    id - id of the food item
    category - different food types (soup, salad, entree, box, dessert, elixir, beverage)
    name - name of the food item
    ingredients - a list of all possible ingredients
    healthy_fact_one - first healthy fact of the food item
    .
    .
    healthy fact_five - last healthy fact
"""


class FoodModel(db.Model):
    __tablename__ = "food"

    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float, primary_key=True)
    category = db.Column(db.String(64), index=True, unique=False)
    name = db.Column(db.String(64), index=True, unique=False)
    withInformation = db.Column(db.String(64), index=True, unique=False)
    picturePath = db.Column(db.String(64), index=True, unique=False)
    iconPath = db.Column(db.String(64), index=True, unique=False)
    ingredients = db.relationship("IngredientModel", backref='related_food')

    def __repr__(self):
        return '<Food {}>'.format(self.name)


"""
Ingredient Model

Contains all the different ingredients a food item could have
None of ingredients should need to be deleted or adjusted, only added

@parameters
    id - ingredient id
    name - name of the ingredient
    icon - a little picture of the ingredient
    food id - the food id the ingredient belongs to
    
because ingredient will have an assoicated food id, for every food item object we create, the database
will be filled with another list of all the ingredients. This should be ok because I dont think the data
is very much
"""


class IngredientModel(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))

    def __repr__(self):
        return '<Ingredients {}>'.format(self.name)


"""
Gift Card Model

Im kind of leaving this blank for now because idk I think an API might come into play
Im leaving some paramters for testing purposes

When a gift card is added to the order, it becomes an item and the gift card is deleted?
I think an API might replace all of this

Please don't focus on this for now, We will focus on this a little bit later

@Parameters
    id - id of the gift card
"""


class GiftCardModel(db.Model):
    __tablename__ = "gift_card"

    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float, primary_key=True)

    def __repr__(self):
        return '<Gift Card {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))