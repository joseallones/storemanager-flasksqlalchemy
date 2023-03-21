import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "store.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class Association(db.Model):
    __table_args__ = (db.UniqueConstraint("store_id", "product_id", "price"),)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id',ondelete='CASCADE'), primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id',ondelete='CASCADE'), primary_key=True, nullable=False)
    price = db.Column('price',db.Numeric(6, 2), nullable=False)
    store = db.relationship('Store', backref=db.backref('associations', cascade='all,delete-orphan'))
    product = db.relationship('Product', backref=db.backref('associations', cascade='all,delete-orphan'))

    def to_json(self):
        return {
            'product_id': self.product_id,
            'product_brand': self.product.brand,
            'store_id': self.store_id,
            'store_name': self.store.name,
            'price': self.price
        }


class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), nullable=False)
    opening_hours = db.Column(db.String(80), nullable=False)
    products = db.relationship("Product", secondary='association')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'opening_hours': self.opening_hours
        }


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80), nullable=False)
    type_product = db.Column(db.String(80), nullable=False)
    calories = db.Column(db.Numeric(6, 2), nullable=False)
    satured_fat_percentage = db.Column(db.Numeric(4, 2), nullable=False)
    sugar_percentage = db.Column(db.Numeric(4, 2), nullable=False)
    __table_args__ = (db.UniqueConstraint('brand', 'type_product'),)

    stores = db.relationship('Store', secondary='association')

    def to_json(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'type_product': self.type_product,
            'calories': self.calories,
            'satured_fat_percentage': self.satured_fat_percentage,
            'sugar_percentage': self.sugar_percentage,
        }