from app import app, db
from flask import session, Session
from flask_restful import Resource, Api, reqparse
from app.models import SystemModel, AdminModel, UserModel, ItemModel, OrderModel, PackageModel, FoodModel, IngredientModel, GiftCardModel
from flask import jsonify, abort
from sqlalchemy.exc import DatabaseError
from app.serializers import system_schema_many, admin_schema_many, user_schema_many, item_schema, item_schema_many, order_schema_many, package_schema_many, food_schema_many, ingredient_schema_many, gift_card_schema_many

from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import UserModel
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, EditProfileForm
from app.forms import PostForm
from app import facebook_blueprint, facebook
from app import google_blueprint, google
import stripe

api = Api(app)
app.register_blueprint(facebook_blueprint, url_prefix='/facebook_login')
app.register_blueprint(google_blueprint, url_prefix='/google_login')

@app.route('/google83147c170400ef36.html')
def verify_google():
    return render_template('google83147c170400ef36.html')

public_key = 'pk_test_Fs2ousnaCNa2XTKGWaW92AIZ00GeY4lpyM'
private_key = 'sk_test_gFsB8Xw8duRIDbERY87hO38u009Zp6jexQ'

stripe.api_key = private_key

@app.route('/pay_item')
def pay_item():
    return render_template('pay_item.html', public_key=public_key)

@app.route('/pay', methods=['POST'])
def pay():
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    charge = stripe.Charge.create(
        customer=customer.id, 
        amount=9900, 
        currency='usd', 
        description='Elixir'
    )

    return redirect(url_for('index'))

@app.route('/delete_cart_item')

@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text

    user = UserModel.query.filter_by(username=resp.json()["name"]).first()

    # Add user to the database if not already there
    if user is None:
        user = UserModel(username=resp.json()["name"])
        db.session.add(user)
        db.session.commit()
        user = UserModel.query.filter_by(username=resp.json()["name"]).first()

    login_user(user)
    return render_template('index.html')

@app.route('/facebook_login')
def facebook_login():

    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    resp = facebook.get("/me")
    assert resp.ok, resp.text
    
    user = UserModel.query.filter_by(username=resp.json()["name"]).first()

    # Add user to the database if not already there
    if user is None:
        user = UserModel(username=resp.json()["name"])
        db.session.add(user)
        db.session.commit()
        user = UserModel.query.filter_by(username=resp.json()["name"]).first()

    login_user(user)
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/cart', methods=['GET', 'POST'])
def cart():

    subtotal = 0

    try:
        user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
        print(user)

        for item in user.items:
            subtotal = subtotal + (item.cost * item.quantity)
        
        subtotal = round(subtotal, 2)
        tax = subtotal * .0825
        tax = round(tax, 2)
        total = tax + subtotal
        total = round(total, 2)

        return render_template('cart.html', user_items = user.items, num_user_items = len(user.items), subtotal=subtotal, tax = tax, total = total)
    
    except:
        print(" \n\n------------- PRINTING ITEMS ------------- ")
        for item in session["items"]:
            print(item, "\n\n")

        for item in session["items"]:
            subtotal = subtotal + item['cost']
        
        subtotal = round(subtotal, 2)
        tax = subtotal * .0825
        tax = round(tax, 2)
        total = tax + subtotal
        total = round(total, 2)

        return render_template('cart.1.html', food_items = session["items"], subtotal = subtotal, tax = tax, total = total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    return render_template('checkout.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    food = FoodModel.query.all()
    food.sort(key=lambda x: x.id)
    #Query all food items for the menu
    return render_template('menu.html', food=food)

@app.route('/packages', methods=['GET', 'POST'])
def packages():
    food = FoodModel.query.all()
    food.sort(key=lambda x: x.id)
    #Query all food items for the menu
    return render_template('packages.html', food=food)

@app.route('/gift', methods=['GET', 'POST'])
def gift():
    return render_template('gift.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserModel(first_name=form.first_name.data, email=form.email.data)
        user.username = user.email
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
    return render_template('profile.html', user=user)

@app.route('/orders', methods=['GET'])
@login_required
def orders():
    user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
    return render_template('orders.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.address_line_1 = form.address_line_1.data
        current_user.address_line_2 = form.address_line_2.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.zip_code = form.zip_code.data
        current_user.phone_number = form.phone_number.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.address_line_1.data = current_user.address_line_1
        form.address_line_2.data = current_user.address_line_2
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.zip_code.data = current_user.zip_code
        form.phone_number.data = current_user.phone_number
        #return redirect(url_for('profile'))
    return render_template('edit_profile.html', title='Edit Profile', form=form, user=user)
        

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

class Food(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)
        parser.add_argument('cost', type=float)
        parser.add_argument('category', type=str)
        parser.add_argument('withInformation', type=str)
        parser.add_argument('picturePath', type=str)
        parser.add_argument('iconPath', type=str)
        self.args = parser.parse_args()

    def get(self):
        food = FoodModel.query.all()
        return jsonify(food=food_schema_many.dump(food).data) 

    def post(self):
        try:
            new_food = FoodModel(**self.args)
            db.session.add(new_food)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'Food not added to database!')

        return jsonify(message='Food successfully created!')

    def put(self):

        food = FoodModel.query.filter_by(id=self.args['id']).first()

        if food:
            try:
                food.id = self.args['id']
                food.name = self.args['name']
                food.cost = self.args['cost']
                food.category = self.args['category']
                food.withInformation = self.args['withInformation']
                food.picturePath = self.args['picturePath']
                food.iconPath = self.args['iconPath']
                db.session.commit()
            except DatabaseError:
                return abort(501, 'The food was not updated!')

            return jsonify(message="Food was successfully updated!")

        else:
            return abort(500, 'The food did not exist')

    def delete(self):
        food = FoodModel.query.filter_by(id=self.args['id']).first()

        if food:
            try:
                db.session.delete(food)
                db.session.commit()
            except DatabaseError:
                return abort(502, 'The food was not deleted')

            return jsonify(message="The food was successfully deleted")

        else:
            return abort(503, 'The food did not exist')

class Ingredient(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type = str)
        parser.add_argument('food_id', type=int)

        self.args = parser.parse_args()

    def get(self):
        ingredients = IngredientModel.query.all()
        return jsonify(ingredients=ingredient_schema_many.dump(ingredients).data) 

    def post(self):
        try:
            new_ingredient = IngredientModel(**self.args)
            db.session.add(new_ingredient)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'Ingredient not added to database!')

        return jsonify(message='Ingredient successfully created!')

    def put(self):

        ingredient = IngredientModel.query.filter_by(id=self.args['id']).first()

        if ingredient:
            try:
                ingredient.id = self.args['id']
                ingredient.name = self.args['name']
                db.session.commit()
            except DatabaseError:
                return abort(501, 'The ingredient was not updated!')

            return jsonify(message="Ingredient was successfully updated!")

        else:
            return abort(500, 'The ingredient did not exist')

    def delete(self):
        ingredient = IngredientModel.query.filter_by(id=self.args['id']).first()

        if ingredient:
            try:
                db.session.delete(ingredient)
                db.session.commit()
            except DatabaseError:
                return abort(502, 'The ingredient was not deleted')

            return jsonify(message="The ingredient was successfully deleted")

        else:
            return abort(503, 'The ingredient did not exist')


class CartItem(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', type=str)
        parser.add_argument('quantity', type=int)
        parser.add_argument('cost', type=int)
        parser.add_argument('id', type=int)
        parser.add_argument('picture_path', type=str)

        self.args = parser.parse_args()
    
    def get(self):
        user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
        return jsonify(items=user.items) 
    
    def post(self):

        try:
            print("Trying to make cart item for user")

            # Query for the user
            user = UserModel.query.filter_by(username=current_user.username).first_or_404() 

            # Make a new item
            new_item = ItemModel(**self.args)

            # Relate the item back to the user?
            new_item.user_id = current_user.id

            # Add to db
            db.session.add(new_item)
            db.session.commit()
        except:
            print("Trying to make cart item for guest")
            
            # Make the item
            new_item = ItemModel(**self.args)

            # JSONify the item
            jsonified_item = item_schema.dump(new_item)[0]
            print("\n\nMY JSON SHIIIIT ------ ", jsonified_item, "\n\n")

            try:
                # Get the guest cart
                guest_cart = session["items"]

                # Add the item
                guest_cart.append(jsonified_item)

                # Update session
                session["items"] = guest_cart

            except:
                # If we need to make a new session instance of items
                session["items"] = []
                
                # Add the item to the guest cart
                guest_cart = session["items"]
                guest_cart.append(jsonified_item)
                
                # Set the session equal to the guest cart
                session["items"] = guest_cart
        
        return jsonify(message='Cart item successfully created!')

class UserClass(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        # parser.add_argument('name', type=str)
        # parser.add_argument('quantity', type=int)
        # parser.add_argument('cost', type=int)
        # parser.add_argument('id', type=int)
        # parser.add_argument('picture_path', type=str)

        self.args = parser.parse_args()
    
    def get(self):
        user = UserModel.query.all()
        return jsonify(users = user_schema_many.dump(user).data) 

class GetNextItemId(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        self.args = parser.parse_args()
    
    def get(self):
        items = ItemModel.query.all()
        if(len(items) is 0):
            next_item_id = 1
        else:
            next_item_id = len(items) + 1
        """
        Need to check that the number of items + 1 does not have an id in the databsae
        (so that no two items have the same id)
        if it does exist, check what number between 1 and len(items) is an id that does not exist and give that item that id number

        """

        return jsonify(next_item_id=next_item_id)








api.add_resource(UserClass, '/user')
api.add_resource(CartItem, '/user/cart')
api.add_resource(GetNextItemId, '/items/get_next_id')
api.add_resource(Food, '/food')
api.add_resource(Ingredient, '/food/ingredients')
