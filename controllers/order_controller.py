from flask import Blueprint, request, jsonify
from models.order import Order

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(Order.get_orders())

@order_bp.route('/orders', methods=['POST'])
def place_order():
    data = request.json
    new_order = Order(**data)
    Order.add_order(new_order.to_dict())
    return jsonify({"message": "Order placed successfully"}), 201