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
from app.forms import RegistrationForm
from app.forms import PostForm


api = Api(app)

# TODO - LOGIN!
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# 

"""
We probably wont use any of this but it is a good reference.


class CreateSystem(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)

        self.args = parser.parse_args()

        super().__init__()

    def post(self):
        try:
            # SystemModel.create(**self.args)
            new_system = SystemModel(**self.args)
            db.session.add(new_system)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'System was not added to the database!')

        return jsonify(message='System successfully created!')


class CreateAdmin(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)

        self.args = parser.parse_args()

        super().__init__()

    def post(self):
        try:
            # AdminModel.create(**self.args)
            new_admin = AdminModel(**self.args)
            db.session.add(new_admin)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'Admin was not added to the database!')

        return jsonify(message='Admin successfully created!')


class CreateUser(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)

        self.args = parser.parse_args()

        super().__init__()

    def post(self):
        try:
            # UserModel.create(**self.args)
            new_User = UserModel(**self.args)
            db.session.add(new_User)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'User was not added to the database!')

        return jsonify(message='User successfully created!')


class SeeAllAdmins(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        admins = SystemModel.query.filter_by(id=self.args['admins']).all()
        return jsonify(admins=admin_schema_many.dump(admins).data)


class SeeAllUsers(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        users = SystemModel.query.filter_by(id=self.args['users']).all()
        return jsonify(users=user_schema_many.dump(users).data)

"""


"""
#Home Page Routes
/get_session
/check_user
/load_user
/create_guest_user

/go_to_home_page
/go_to_menu_menu
/go_to_packages_page
/go_to_gift_card_page
/go_to_order_page
/go_to_login

#Login Page Routes (I imagine we will find an API or something similar on how to do this)
/login

#Menu Page Routes/menu/switch_to_admin_edit)
menu/get_session
menu/check_user
menu/load_user
menu/create_guest_user

/menu/select_soup_item1
.
.
/menu/select_soup_item5
/menu/soup_item1/increment_quantity
/menu/soup_item1/decrement_quantity
/menu/soup_item1/add_to_cart #this will create an item and add the item to users order#

/menu/edit/add_item
/menu/edit/select_item
/menu/edit/delete_item


#Packages Page Routes
package/get_session
package/check_user
package/load_user
package/set_session
package/create_guest_user

/packages/select_package_type
/packages/get_started
/package/3-type
/package/5-type
/package/3-type/item1
/package/5-type/item4
/package/5-type/item4/select_item1
/package/5-type/add_quantity
/package/3-type/add_to_cart


#Gift Card Page Routes
gift_card/get_session
gift_card/check_user
gift_card/load_user
gift_card/set_session
gift_card/create_guest_user

#Order Page Routes
order/get_session
order/check_user
order/load_user
order/set_session
order/create_guest_user

"""