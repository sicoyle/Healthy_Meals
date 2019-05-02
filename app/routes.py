from app import app, db
from flask import session, Session
from flask_restful import Resource, Api, reqparse
from app.models import AdminModel, UserModel, ItemModel, OrderModel, PackageModel, FoodModel, IngredientModel, GiftCardModel
from flask import jsonify, abort
from sqlalchemy.exc import DatabaseError
from app.serializers import admin_schema_many, user_schema_many, item_schema, item_schema_many, order_schema_many, package_schema_many, food_schema_many, ingredient_schema_many, gift_card_schema_many

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
from app.forms import RegistrationForm, EditProfileForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm
from app.forms import PostForm
from app import facebook_blueprint, facebook
from app import google_blueprint, google
import stripe
import random
import re

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

@app.route('/delete_guest_cart_item', methods=['POST'])
def delete_guest_cart_item(): 
    guest_cart = session["items"]
    del guest_cart[int(request.form['index'])]
    session["items"] = guest_cart

    return redirect(url_for('cart'))

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

@app.route('/delete_guest_item', methods=['POST'])
def delete_guest_item():
    index = int(request.form["index"])
    guest_cart = session["items"]

    del guest_cart[index]

    session["items"] = guest_cart
    
    return redirect(url_for('cart'))


@app.route('/delete_user_item', methods=['POST'])
def delete_user_item():
    user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
    index = int(request.form["index"])

    del user.items[index]
    db.session.commit()
    return redirect(url_for('cart'))
    

@app.route('/cart', methods=['GET', 'POST'])
def cart():

    subtotal = 0

    try:
        user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
        print(user)

        for item in user.items:
            subtotal = subtotal + (item.cost * item.quantity)
        
        print("LENGTH: ", len(user.items))
        
        subtotal = round(subtotal, 2)
        tax = subtotal * .0825
        tax = round(tax, 2)
        total = tax + subtotal
        total = round(total, 2)

        return render_template('cart.html', user_items = user.items, num_user_items = len(user.items), subtotal=subtotal, tax = tax, total = total, user = user)
    
    except:
        
        try:
            for item in session["items"]:
                subtotal = subtotal + (item["cost"] * item["quantity"])
        except:
            session["items"] = []

            for item in session["items"]:
                subtotal = subtotal + (item["cost"] * item["quantity"])
        
        subtotal = round(subtotal, 2)
        tax = subtotal * .0825
        tax = round(tax, 2)
        total = tax + subtotal
        total = round(total, 2)

        return render_template('guest_cart.html', food_items = session["items"], subtotal = subtotal, tax = tax, total = total)

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
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            error = 'Incorrect password.'
            if user is None:
                error = 'User not found. Please try a different email address.'
            flash('Invalid username or password')
            return render_template('login.html', title='Sign In', form=form, error=error)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserModel(first_name=form.first_name.data, email=form.email.data)
        user.username = user.email
        if len(form.password.data) < 8:
            error='Make sure your password is at least 8 letters'
            flash('Invalid password.', 'error')
        elif re.search('[0-9]',form.password.data) is None:
            error='Make sure your password has a number in it'
        elif re.search('[A-Z]',form.password.data) is None: 
            error='Make sure your password has a capital letter in it'
        else:
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
    flash('Invalid password.', 'error')
        #return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form, error=error)

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', user=user, image_file=image_file)

@app.route('/orders', methods=['GET'])
@login_required
def orders():
    #admin = AdminModel.query.filter_by(name=current_admin.name).first_or_404() 
    user = UserModel.query.filter_by(username=current_user.username).first_or_404() 

    if request.method == 'GET':
        past_order_items = OrderModel.query.all()
        past_order_items = item_schema_many.dump(past_order_items)
        #return jsonify(past_order_items) 
        return render_template('orders.html', user=user, past_items = user.orders, num_order_items = len(user.orders))
    
    return render_template('orders.html', user=user, past_items = user.orders, num_order_items = len(user.orders))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form.picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', 'picture_fn')
    form_picture.save(picture_path)

    return picture_fn

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    error = None
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
    form = EditProfileForm(request.form)
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.address_line_1 = form.address_line_1.data
        current_user.address_line_2 = form.address_line_2.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        if form.state.data == 'Select State':
            error = "Select a state."
            return render_template('edit_profile.html', title='Edit Profile', form=form, user=user, error=error, image_file=image_file)
        current_user.zip_code = form.zip_code.data
        db.session.commit()
        print("just posted")
        flash('Your changes have been saved.')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.address_line_1.data = current_user.address_line_1
        form.address_line_2.data = current_user.address_line_2
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.zip_code.data = current_user.zip_code
        return render_template('edit_profile.html', title='Edit Profile', form=form, user=user, error=error, image_file=image_file)
    return render_template('profile.html', user=user, error=error, image_file=image_file)

@app.route('/update_guest_item', methods=['PUT'])
def update_guest_item():
    index = int(request.get_json()["index"])
    print("Helller in /update_guest_item route in ROUTES.py**********************************************************************")

    print("index: " , index)

    updated_quantity = int(request.get_json()["updated_quantity"])
    guest_cart = session["items"]
    print("************************", guest_cart)
    print("updated_quantity: " , updated_quantity)
    
    guest_cart[index]['quantity'] = updated_quantity

    subtotal = 0

    print("************************", guest_cart)
    session["items"] = guest_cart
    for item in session["items"]:
            subtotal = subtotal + (item["cost"] * item["quantity"])

    subtotal = round(subtotal, 2)
    tax = subtotal * .0825
    tax = round(tax, 2)
    total = tax + subtotal
    total = round(total, 2)

    return render_template('cart.1.html', food_items = session["items"], subtotal = subtotal, tax = tax, total = total)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    error = None
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            if len(form.password.data) < 8:
                error='Make sure your password is at least 8 letters'
            elif re.search('[0-9]',form.password.data) is None:
                error='Make sure your password has a number in it'
            elif re.search('[A-Z]',form.password.data) is None: 
                error='Make sure your password has a capital letter in it'
            else:
                current_user.set_password(form.password.data)
                db.session.commit()
                flash('Your password has been updated.')
                return redirect(url_for('profile'))
        else:
            error = 'Old password does not match'
            flash('Invalid password.', 'error')
    return render_template("change_password.html", form=form, error=error)

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
        cart_items = ItemModel.query.all()
        cart_items = item_schema_many.dump(cart_items)
        return jsonify(cart_items)  

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


    def put(self):
        print("in put now!")
        print("helllo", request.get_json()['item_index'])
        print("helllo", request.get_json()['updated_quantity'])

        user = UserModel.query.filter_by(username=current_user.username).first_or_404()
        try:
            print("INSIDE THE TRY BLOCK in Routes")
            new_item_index = int(request.get_json()['item_index'])
            new_updated_quantity = int(request.get_json()['updated_quantity'])
    
            item_id = user.items[new_item_index]
            #print("this is item_id")
            #print(item_id)
         
            item_id.quantity = new_updated_quantity
          
            db.session.commit()

        except:
            return abort(502, "Item was not updated in the users cart")

        return jsonify(message="Item was updated in users cart")
        #return render_template('cart.html', user_items = user.items, num_user_items = len(user.items), subtotal=subtotal, tax = tax, total = total)



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


class PlaceUserOrder(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=str)
        parser.add_argument('cost', type=float)
        parser.add_argument('completed', type=bool)

        self.args = parser.parse_args()

    def get(self):
        user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
        return jsonify(orders=user.orders) 

    def post(self):
        print("Trying to make order for user")

        subtotal = 0

        # Query for the user
        user = UserModel.query.filter_by(username=current_user.username).first_or_404() 

        for item in user.items:
            subtotal = subtotal + (item.cost * item.quantity)
        
        subtotal = round(subtotal, 2)
        tax = subtotal * .0825
        tax = round(tax, 2)
        total = tax + subtotal
        total = round(total, 2)

        # Make a new order
        new_order = OrderModel(**self.args)



        # Relate the order back to the user?
        new_order.admin_id = 0
        new_order.user_id = current_user.id
        new_order.order_items = user.items
        new_order.completed = False
        new_order.cost = total

        print("did it")          

        # Add to db
        db.session.add(new_order)
        db.session.commit()

class GetNextOrderID(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        self.args = parser.parse_args()
    
    def get(self):
        orders = OrderModel.query.all()
        if(len(orders) is 0):
            next_order_id = 1
        else:
            next_order_id = len(orders) + 1
        """
        Need to check that the number of items + 1 does not have an id in the databsae
        (so that no two items have the same id)
        if it does exist, check what number between 1 and len(items) is an id that does not exist and give that item that id number

        """

        return jsonify(next_order_id=next_order_id)

class Admins(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)

        self.args = parser.parse_args()
    
    def get(self):
        admin = AdminModel.query.all()
        return jsonify(admin=admin_schema_many.dump(admin).data) 

    def post(self):
        try:
            new_admin = AdminModel(**self.args)
            db.session.add(new_admin)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'Admin not added to database!')

        return jsonify(message='Admin successfully created!')


        

api.add_resource(GetNextOrderID, '/orders/get_next_id')
api.add_resource(PlaceUserOrder, '/place_user_order')
api.add_resource(UserClass, '/user')
api.add_resource(CartItem, '/user/cart')
api.add_resource(GetNextItemId, '/items/get_next_id')
api.add_resource(Food, '/food')
api.add_resource(Ingredient, '/food/ingredients')
api.add_resource(Admins, '/admin')
