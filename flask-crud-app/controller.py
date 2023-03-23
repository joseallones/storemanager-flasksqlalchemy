
from model import db, Association, Product, Store
from flask import jsonify
from flask import request


def welcome():
    return "Welcome to the store API!"


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



def get_products_store(id):

    try:
        store = Store.query.get(id)
        if store is None:
            return "Not found store", 400
        return jsonify([assoc.to_json() for assoc in store.associations])

    except Exception as e:
        return "Bad request", 400