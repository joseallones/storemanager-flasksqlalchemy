import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import warnings


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


@app.route('/product', methods=["POST"])
def add_product():

    try:
        product = Product(brand=request.json['brand'],
                          type_product=request.json['type_product'],
                          calories=request.json['calories'],
                          satured_fat_percentage=request.json['satured_fat_percentage'],
                          sugar_percentage=request.json['sugar_percentage'])

        if ('id' in request.json):
            product.id = request.json['id']

        db.session.add(product)
        db.session.commit()

        return jsonify(product.to_json())

    except Exception as e:
        print("Failed to add product " + str(e))
        db.session.rollback()
        return "Invalid product data", 422


@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):

    if not request.json:
        return "Invalid product data", 400
    product = Product.query.get(id)

    if product is None:
        return "Not found", 400

    try:
        product.brand = request.json.get('brand', product.brand)
        product.type_product = request.json.get('type_product', product.type_product)
        product.calories = request.json.get('calories', product.calories)
        product.satured_fat_percentage = request.json.get('satured_fat_percentage', product.satured_fat_percentage)
        product.sugar_percentage = request.json.get('sugar_percentage', product.sugar_percentage)
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_json())
    except Exception as e:
        db.session.rollback()
        return "Invalid product data", 422




@app.route('/product/<int:id>/price', methods=['PUT'])
def update_price(id):

    try:
        if not request.json:
            return "Invalid product data", 400

        product = Product.query.get(id)
        if product is None:
            return "Not found product", 400

        store = Store.query.get(request.json.get('store_id'))
        if store is None:
            return "Not found store", 400

        assoc = Association.query.filter_by(store_id = store.id, product_id = product.id).first()

        if(assoc):
            assoc.price = request.json.get('price')
        else:
            assoc = Association(price=request.json.get('price'))
            assoc.product = product
            store.associations.append(assoc)

        db.session.add_all([store])
        db.session.add_all([product])

        db.session.commit()

        return jsonify(assoc.to_json())

    except Exception as e:
        db.session.rollback()
        return "Invalid data", 422


@app.route('/store', methods=["POST"])
def add_store():

    try:
        store = Store(name=request.json['name'],
                      address=request.json['address'],
                      opening_hours=request.json['opening_hours'])

        if('id' in request.json):
            store.id = request.json['id']

        db.session.add(store)
        db.session.commit()

        return jsonify(store.to_json())

    except Exception as e:
        db.session.rollback()
        return "Invalid product data", 422


@app.route('/store/<int:id>/products', methods=["GET"])
def get_products_store(id):

    try:
        store = Store.query.get(id)
        if store is None:
            return "Not found store", 400
        return jsonify([assoc.to_json() for assoc in store.associations])

    except Exception as e:
        return "Bad request", 400


@app.route('/', methods=["GET"])
def welcome():
    return "Welcome to the store API!"

warnings.filterwarnings("ignore")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port= 5001)