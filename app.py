"""
Flask SQLAlchemy REST API

REST API With Flask & SQL Alchemy

Homepage and documentation:


Copyright (c) 2019, Marcus Mariano.
License: MIT (see LICENSE for details)
"""

import os

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Product class/model
class Product(db.Model):
    """Database."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# Product class/model
class ProductSchema(ma.Schema):
    """Schema."""
    class Meta:
        """."""
        fields = ('id', 'description', 'price', 'qty')

# Init schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)


# Create a Product
@app.route("/api/v1.0/product",  methods=['POST'])
def add_product():
    """Create product."""
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


@app.route("/api/v1.0/product",  methods=['GET'])
def get_products():
    """Get all Product."""
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)


@app.route("/api/v1.0/product/<int:id>",  methods=['GET'])
def get_product(id):
    """Get simgle Product."""
    product = Product.query.get(id)    
    return product_schema.jsonify(product)

@app.route("/api/v1.0/product/<int:id>",  methods=['PUT'])
def update_product(id):
    """Update a Product."""
    product = Product.query.get(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return product_schema.jsonify(product)

@app.route("/api/v1.0/product/<int:id>",  methods=['DELETE'])
def delete_product(id):
    """Delete Product."""
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
     
    return product_schema.jsonify(product)


# Run Server
if __name__ == "__main__":
    app.run(debug=True)
