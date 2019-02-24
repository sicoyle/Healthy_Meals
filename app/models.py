from app import db


class AdminModel(db.Model):

    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)

    def __repr__(self):
        return '<Admin {}>'.format(self.name)


class UserModel(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class ItemModel(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    cost = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.name)




class OrderModel(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship('ItemModel', backref='order_items')
    cost = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Order {}>'.format(self.name)

