from app import app, db
from flask import session, Session
from flask_restful import Resource, Api, reqparse
from app.models import SystemModel, AdminModel, UserModel, ItemModel, OrderModel, PackageModel, FoodModel, IngredientModel, GiftCardModel
from flask import jsonify, abort
from sqlalchemy.exc import DatabaseError
from app.serializers import system_schema_many, admin_schema_many, user_schema_many, item_schema_many, order_schema_many, package_schema_many, food_schema_many, ingredient_schema_many, gift_card_schema_many

from flask import render_template, flash, redirect, url_for
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

api = Api(app)
app.register_blueprint(facebook_blueprint, url_prefix='/facebook_login')
app.register_blueprint(google_blueprint, url_prefix='/google_login')

@app.route('/google83147c170400ef36.html')
def verify_google():
    return render_template('google83147c170400ef36.html')

# @app.route('/delete_guest_cart_item', methods=['POST'])
# def delete_guest_cart_item(): 
#     guest_cart = session["items"]
#     del guest_cart[int(request.form['index'])]
#     session["items"] = guest_cart

#     return redirect(url_for('cart'))

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
    user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
    print(user)

    subtotal = 0

 

    for item in user.items:
        print(item.cost)
        print(item.quantity)
        subtotal = subtotal + (item.cost * item.quantity)

    
    subtotal = round(subtotal, 2)
    tax = subtotal * .0825
    tax = round(tax, 2)
    total = tax + subtotal
    total = round(total, 2)

    return render_template('cart.html', user_items = user.items, num_user_items = len(user.items), subtotal=subtotal, tax = tax, total = total)

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
    form = EditProfileForm(request.form)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.address_line_1 = form.address_line_1.data
        current_user.address_line_2 = form.address_line_2.data
        current_user.city = form.city.data
        current_user.state = form.state.data
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
        return render_template('edit_profile.html', title='Edit Profile', form=form, user=user)
    return render_template('profile.html', user=user)

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
        print("Were in post nowwww!")
        user = UserModel.query.filter_by(username=current_user.username).first_or_404() 
        try:
            print("INSIDE THE TRY BLOCK")
            new_item = ItemModel(**self.args)
            new_item.user_id = current_user.id
            # quantity = request.form.get('updated_quantity')
            # item_index_in_cart = request.form['index']
            # print(quantity)
            # print(item_index_in_cart)
            db.session.add(new_item)
            db.session.commit()
        except:
            return abort(502, "Item was not added to the users cart")
        
        return jsonify(message='Cart item successfully created!')

    # def put(self):
    #     print("in put now!")

    #     user = UserModel.query.filter_by(username=current_user.username).first_or_404()
    #     try:
    #         print("INSIDE THE TRY BLOCK in Routes")
    #         #cart = session["items"]
    #         #user.items.id = int(request.form['index'])
    #         #user.items.quantity = int(request.form['updated_quantity'])
    #         #session["items"] = cart
    #         quantity = request.form.get('updated_quantity')
    #         item_index_in_cart = request.form['index']
    #         console.log(quantity)
    #         console.log(item_index_in_cart)
    #        # db.session.commit()
    #     except:
    #         return abort(502, "Item was not updated in the users cart")

    #     return jsonify(message='Cart item successfully updated!')

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