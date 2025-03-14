from flask import Blueprint, jsonify, request
from models.user import Customer
from models.item import Item

customer_bp = Blueprint("customer", __name__)

customers = Customer.load_customers()
items = Item.load_items()

# Add item to cart
@customer_bp.route("/customer/cart/add", methods=["POST"])
def add_to_cart():
    """Add an item to the customer's cart."""
    data = request.json
    print(data)
    customer_id = data.get("customer_id")
    item_id = data.get("item_id")
    quantity = int(data.get("quantity", 1))
    
    customer = next((c for c in customers if c.user_id == customer_id), None)
    
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    item = next((i for i in items if i.item_id == item_id), None)
    print(f"Searching for item_id: {item_id}")
    print("Available item IDs:", [i.item_id for i in items])
    print("Item found:", item.item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    if not customer.add_to_cart(item, quantity):
        return jsonify({"error": "Not enough stock available"}), 400

    Customer.save_customers(customers)
    return jsonify({"message": "Item added to cart", "cart": customer.view_cart()})


# Remove item from cart
@customer_bp.route("/customer/cart/remove", methods=["POST"])
def remove_from_cart():
    """Remove an item from the customer's cart."""
    data = request.json
    customer_id = data.get("customer_id")
    item_id = data.get("item_id")
    quantity = int(data.get("quantity", 1))

    customer = next((c for c in customers if c.user_id == customer_id), None)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    item = next((i for i in items if i.item_id == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    if not customer.remove_from_cart(item, quantity):
        return jsonify({"error": "Item not found in cart"}), 400

    Customer.save_customers(customers)
    return jsonify({"message": "Item removed from cart", "cart": customer.view_cart()})


# View cart
@customer_bp.route("/customer/cart", methods=["GET"])
def view_cart():
    """Return all items in the customer's cart."""
    customer_id = request.args.get("customer_id")

    customer = next((c for c in customers if c.user_id == customer_id), None)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify({"cart": customer.view_cart()})


# Checkout (Place order)
@customer_bp.route("/customer/cart/checkout", methods=["POST"])
def checkout():
    """Place an order and clear the cart."""
    data = request.json
    customer_id = data.get("customer_id")

    customer = next((c for c in customers if c.user_id == customer_id), None)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    if not customer.place_order():
        return jsonify({"error": "Cart is empty. Cannot place order."}), 400

    Customer.save_customers(customers)
    return jsonify({"message": "Order placed successfully", "order_history": customer.view_order_history()})


# View order history
@customer_bp.route("/customer/orders", methods=["GET"])
def view_orders():
    """Return all past orders for the customer."""
    customer_id = request.args.get("customer_id")

    customer = next((c for c in customers if c.user_id == customer_id), None)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify({"order_history": customer.view_order_history()})