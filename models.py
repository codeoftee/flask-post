# models.py
from index import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(200), unique=True, index=True)
    password_hash = db.Column(db.String(200))
    balance = db.Column(db.Numeric(10, 2), default=0)
    joined = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    image = db.Column(db.Text)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Product {}: Price {}>'.format(self.title, self.price)
