from app import app, db
from flask_restful import Resource, Api, reqparse
from app.models import AdminModel, UserModel, ItemModel, OrderModel, PackageModel
from flask import jsonify, abort
from sqlalchemy.exc import DatabaseError
from app.serializers import admin_schema_many, user_schema_many, item_schema_many, order_schema_many, package_schema_many

api = Api(app)


class Admin(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        admins = AdminModel.query.all()
        return jsonify(admins=admin_schema_many.dump(admins).data)

    def post(self):
        try:
            # AdminModel.create(**self.args)
            new_admin = AdminModel(**self.args)
            db.session.add(new_admin)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'Admin was not added to the database!')

        return jsonify(message='Admin successfully created!')

    def put(self):

        admin = AdminModel.query.filter_by(id=self.args['id']).first()

        if admin:
            try:
                admin.id = self.args['id']
                admin.name = self.args['name']
                db.session.commit()
            except DatabaseError:
                return abort(501, 'The admin was not updated!')

            return jsonify(message="Admin was successfully updated!")

        else:
            return abort(500, 'The admin did not exist')

    def delete(self):
        admin = AdminModel.query.filter_by(id=self.args['id']).first()

        if admin:
            try:
                db.session.delete(admin)
                db.session.commit()
            except DatabaseError:
                return abort(502, 'The admin was not deleted')

            return jsonify(message="The admin was successfully deleted")

        else:
            return abort(503, 'The admin did not exist')


class User(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        users = UserModel.query.all()
        return jsonify(users=user_schema_many.dump(users).data)

    def post(self):
        try:
            # AdminModel.create(**self.args)
            new_user = UserModel(**self.args)
            db.session.add(new_user)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'User was not added to the database!')

        return jsonify(message='User successfully created!')

    def put(self):

        user = UserModel.query.filter_by(id=self.args['id']).first()

        if user:
            try:
                user.id = self.args['id']
                user.name = self.args['name']
                db.session.commit()
            except DatabaseError:
                return abort(501, 'The user was not updated!')

            return jsonify(message="User was successfully updated!")

        else:
            return abort(500, 'The user did not exist')

    def delete(self):
        user = UserModel.query.filter_by(id=self.args['id']).first()

        if user:
            try:
                db.session.delete(user)
                db.session.commit()
            except DatabaseError:
                return abort(502, 'The user was not deleted')

            return jsonify(message="The user was successfully deleted")

        else:
            return abort(503, 'The user did not exist')

class Item(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('name', type=str)
        parser.add_argument('cost', type=float)
        parser.add_argument('order_id', type=int)
        parser.add_argument('package_id', type=int)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        items = ItemModel.query.all()
        return jsonify(items=item_schema_many.dump(items).data)

    def post(self):
        try:
            # AdminModel.create(**self.args)
            new_item = ItemModel(**self.args)
            db.session.add(new_item)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'Item was not added to the database!')

        return jsonify(message='Item successfully created!')

    def put(self):

        item = ItemModel.query.filter_by(id=self.args['id']).first()

        if item:
            try:
                item.id = self.args['id']
                item.name = self.args['name']
                item.cost = self.args['cost']
                item.order_id = self.args['order_id']
                item.package_id = self.args['package_id']

                db.session.commit()
            except DatabaseError:
                return abort(501, 'The item was not updated!')

            return jsonify(message="Item was successfully updated!")

        else:
            return abort(500, 'The item did not exist')

    def delete(self):
        item = ItemModel.query.filter_by(id=self.args['id']).first()

        if item:
            try:
                db.session.delete(item)
                db.session.commit()
            except DatabaseError:
                return abort(502, 'The item was not deleted')

            return jsonify(message="The item was successfully deleted")

        else:
            return abort(503, 'The item did not exist')


class Order(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('cost', type=float)

        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        orders = OrderModel.query.all()
        return jsonify(orders=order_schema_many.dump(orders).data)

    def post(self):
        try:
            # AdminModel.create(**self.args)
            new_order = OrderModel(**self.args)
            db.session.add(new_order)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'Order was not added to the database!')

        return jsonify(message='Order successfully created!')

    def put(self):

        order = OrderModel.query.filter_by(id=self.args['id']).first()

        if order:
            try:
                order.id = self.args['id']
                order.cost = self.args['cost']
                db.session.commit()
            except DatabaseError:
                return abort(501, 'The order was not updated!')

            return jsonify(message="Order was successfully updated!")

        else:
            return abort(500, 'The order did not exist')

    def delete(self):
        order = OrderModel.query.filter_by(id=self.args['id']).first()

        if order:
            try:
                db.session.delete(order)
                db.session.commit()
            except DatabaseError:
                return abort(502, 'The order was not deleted')

            return jsonify(message="The order was successfully deleted")

        else:
            return abort(503, 'The order did not exist')


class Package(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()

        parser.add_argument('id', type=int)
        parser.add_argument('cost', type=float)
        parser.add_argument('order_id', type=int)


        self.args = parser.parse_args()

        super().__init__()

    def get(self):
        package = PackageModel.query.all()
        return jsonify(packages=package_schema_many.dump(package).data)

    def post(self):
        try:
            # AdminModel.create(**self.args)
            new_package = PackageModel(**self.args)
            db.session.add(new_package)
            db.session.commit()

        except DatabaseError:
            return abort(500, 'Package was not added to the database!')

        return jsonify(message='Package successfully created!')

    def put(self):

        package = PackageModel.query.filter_by(id=self.args['id']).first()

        if package:
            try:
                package.id = self.args['id']
                package.cost = self.args['cost']
                db.session.commit()
            except DatabaseError:
                return abort(501, 'The package was not updated!')

            return jsonify(message="Package was successfully updated!")

        else:
            return abort(500, 'The package did not exist')

    def delete(self):
        package = PackageModel.query.filter_by(id=self.args['id']).first()

        if package:
            try:
                db.session.delete(package)
                db.session.commit()
            except DatabaseError:
                return abort(502, 'The package was not deleted')

            return jsonify(message="The package was successfully deleted")

        else:
            return abort(503, 'The package did not exist')


# Admin Routes
api.add_resource(Admin, '/admin')
api.add_resource(User, '/user')
api.add_resource(Item, '/item')
api.add_resource(Order, '/order')
api.add_resource(Package, '/package')