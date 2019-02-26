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
    cost = db.Column(db.Float, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'))

    def __repr__(self):
        return '<Item {}>'.format(self.name)


class OrderModel(db.Model):
    __tablename__ = "order"

    id = db.Column(db.Integer, primary_key=True)
    order_items = db.relationship('ItemModel', backref='related_order')
    order_packages = db.relationship('PackageModel', backref='related_order')
    cost = db.Column(db.Float, primary_key=True)

    def __repr__(self):
        return '<Order {}>'.format(self.name)

class PackageModel(db.Model):
    __tablename__ = "package"

    id = db.Column(db.Integer, primary_key=True)
    cost = db.Column(db.Float, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    package_items = db.relationship('ItemModel', backref='related_package')

    def __repr__(self):
        return '<Package {}>'.format(self.name)




