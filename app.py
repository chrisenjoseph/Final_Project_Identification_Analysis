from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

# Home Route
@app.route('/')
def home():
    return jsonify({
        "message": "FinalProjectMax3 API is running"
    })

# GET all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()

    result = []

    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "price": product.price
        })

    return jsonify(result)

# POST new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()

    new_product = Product(
        name=data['name'],
        price=data['price']
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "message": "Product added successfully"
    }), 201

# GET all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()

    result = []

    for order in orders:
        result.append({
            "id": order.id,
            "customer_name": order.customer_name,
            "product_id": order.product_id
        })

    return jsonify(result)

# POST new order
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()

    new_order = Order(
        customer_name=data['customer_name'],
        product_id=data['product_id']
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        "message": "Order created successfully"
    }), 201

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)