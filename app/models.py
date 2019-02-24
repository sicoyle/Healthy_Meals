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
    firstName = db.Column(db.String(64), index=True, unique=False)
    lastName = db.Column(db.String(64), index=True, unique=False)
    middleName = db.Column(db.String(64), index=True, unique=False)
    phoneNumber = db.Column(db.String(64), index=True, unique=False)
    address = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(64), index=True, unique=False)


    def __repr__(self):
        return '<User {}>'.format(self.name)


