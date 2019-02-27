from app import app, db
from flask_restful import Resource, Api, reqparse
from app.models import SystemModel, AdminModel, UserModel, ItemModel, OrderModel, PackageModel, FoodModel, IngredientModel, GiftCardModel
from flask import jsonify, abort
from sqlalchemy.exc import DatabaseError
from app.serializers import system_schema_many, admin_schema_many, user_schema_many, item_schema_many, order_schema_many, package_schema_many, food_schema_many, ingredient_schema_many, gift_card_schema_many

api = Api(app)


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




#System Routes
api.add_resource(CreateSystem, '/create_system')
api.add_resource(CreateAdmin, '/create_system')
api.add_resource(CreateUser, '/create_system')
api.add_resource(SeeAllUsers, '/create_system')

"""
# Admin Routes
api.add_resource(AddFoodItem, '/admin/add_food_item')

api.add_resource(DeleteFoodItem, '/admin/delete_food_item')
api.add_resource(AddIngredient, '/admin/add_ingredient')
api.add_resource(DeleteIngredient, '/admin/delete_ingredient')

api.add_resource(SeeAllOrders, '/admin/see_all_orders')
api.add_resource(SeeActiveOrders, '/admin/see_active_orders')
api.add_resource(SeeCompletedOrders, '/admin/see_completed_orders')

#User Routes

#Item Routes

#Package Routes

#Food Routes

#Ingredient Routes

#Gift Card Routes

"""