from marshmallow_sqlalchemy import ModelSchema
from app.models import AdminModel, UserModel, ItemModel, OrderModel, PackageModel, FoodModel, IngredientModel, GiftCardModel


class AdminSchema(ModelSchema):
    class Meta:
        model = AdminModel


class UserSchema(ModelSchema):
    class Meta:
        model = UserModel


class ItemSchema(ModelSchema):
    class Meta:
        model = ItemModel


class PackageSchema(ModelSchema):
    class Meta:
        model = PackageModel


class OrderSchema(ModelSchema):
    class Meta:
        model = OrderModel

class FoodSchema(ModelSchema):
    class Meta:
        model = FoodModel

class IngredientSchema(ModelSchema):
    class Meta:
        model = IngredientModel

class GiftCardSchema(ModelSchema):
    class Meta:
        model = GiftCardModel


admin_schema_many = AdminSchema(many=True)
admin_schema = AdminSchema()

user_schema_many = UserSchema(many=True)
user_schema = UserSchema()

item_schema_many = ItemSchema(many=True)
item_schema = ItemSchema()

package_schema_many = PackageSchema(many=True)
package_schema = PackageSchema()

order_schema_many = OrderSchema(many=True)
order_schema = OrderSchema()

food_schema_many = FoodSchema(many=True)
food_schema = FoodSchema()

ingredient_schema_many = IngredientSchema(many=True)
ingredient_schema = IngredientSchema()

gift_card_schema_many = GiftCardSchema(many=True)
gift_card_schema = GiftCardSchema()