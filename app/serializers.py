from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema
from app.models import AdminModel, UserModel


#ma = Marshmallow()

class UserSchema(ModelSchema):
    class Meta:
        model = UserModel

class AdminSchema(ModelSchema):
    class Meta:
        model = AdminModel

user_schema_many = UserSchema(many=True)
user_schema = UserSchema()

admin_schema_many = AdminSchema(many=True)
admin_schema = AdminSchema()

