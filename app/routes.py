from app import app, db
from flask_restful import Resource, Api, reqparse
from app.models import AdminModel, UserModel
from flask import jsonify, abort
from sqlalchemy.exc import DatabaseError
from app.serializers import admin_schema_many, user_schema_many,  user_schema

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
        print(admins)
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
                return abort(502, 'The item was not deleted')

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
        print(users)
        return jsonify(users=user_schema_many.dump(users).data)

    def post(self):
        try:
            # UserModel.create(**self.args)
            new_user = AdminModel(**self.args)
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
                return abort(502, 'The item was not deleted')

            return jsonify(message="The user was successfully deleted")

        else:
            return abort(503, 'The user did not exist')



# Routes
api.add_resource(Admin, '/admin')
api.add_resource(User, '/user')
