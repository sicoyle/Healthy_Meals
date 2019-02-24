from marshmallow_sqlalchemy import ModelSchema
from app.models import AdminModel, UserModel, ItemModel, OrderModel

class UserSchema(ModelSchema):
    class Meta:
        model = UserModel

class AdminSchema(ModelSchema):
    class Meta:
        model = AdminModel

class ItemSchema(ModelSchema):
    class Meta:
        model = ItemModel

class OrderSchema(ModelSchema):
    class Meta:
        model = OrderModel

user_schema_many = UserSchema(many=True)
user_schema = UserSchema()

admin_schema_many = AdminSchema(many=True)
admin_schema = AdminSchema()

item_schema_many = ItemSchema(many=True)
item_schema = ItemSchema()

order_schema_many = OrderSchema(many=True)
order_schema = OrderSchema()