from flask import Blueprint, jsonify, request 
from models.customer import Customer
from models.cart import Cart
from models.item import Item
from services.user_service import get_customer_by_email,get_all_users
from services.menu_service import get_all_menu
from services.cart_service import return_cart
from utils.file_handler import FileHandler

customer_bp = Blueprint("customer", __name__)

# Add item to cart
@customer_bp.route("/cart/add", methods=["POST"])
def add_to_cart():
    """Add an item to the customer's cart."""
    data = request.json
    user_id = data["email"]
    
    verify_user = get_customer_by_email(user_id)
    if not verify_user:
        return jsonify({"error" : "Invalid customer id"}), 404 
    customer = Customer(verify_user["name"], verify_user["email"], verify_user["password"], verify_user["order_history"], Cart(return_cart()))

    item_id = data["name"]
    item_amount = int(data.get("quantity", 1))
    item = None
    menu_all = get_all_menu()
    for menu in menu_all:
        if menu["name"] == item_id:
            item = Item(**menu)

    if not item:
        return jsonify({"error": "Invalid item"}), 404

    if not customer.add_to_cart(item, item_amount):
        return jsonify({"error": "Not enough stock available"}), 400
        
    return jsonify({"message": "Item added to cart", "cart": customer.view_cart()}), 200

# Remove item from cart
@customer_bp.route("/cart/remove", methods=["POST"])
def remove_from_cart():
    """Remove an item from the customer's cart."""
    data = request.json
    user_id = data["email"]
    
    verify_user = get_customer_by_email(user_id)
    if not verify_user:
        return jsonify({"error" : "Invalid customer id"}), 404 
    
    customer = Customer(verify_user["name"], verify_user["email"], verify_user["password"], verify_user["order_history"], Cart(return_cart()))

    item_id = data["name"]
    item_amount = int(data.get("quantity", 1))
    item = None
    menu_all = get_all_menu()
    for menu in menu_all:
        if menu["name"] == item_id:
            item = Item(**menu)

    if not item:
        return jsonify({"error": "Invalid item"}), 404
    print(customer.view_cart())
    if not customer.remove_from_cart(item, item_amount):
        return jsonify({"error": "Item not found in cart"}), 400
    
    return jsonify({"message": "Item removed from cart", "cart": customer.view_cart()}) , 200


# View cart
@customer_bp.route("/cart/view", methods=["GET"])
def view_cart():
    """Return all items in the customer's cart."""
    data = request.json
    user_id = data["email"]
    
    verify_user = get_customer_by_email(user_id)
    if not verify_user:
        return jsonify({"error" : "Invalid customer id"}), 404 
    customer = Customer(verify_user["name"], verify_user["email"], verify_user["password"], verify_user["order_history"], Cart(return_cart()))

    return jsonify( {"message" : "View cart items ","data": customer.view_cart()}) , 200


# Checkout (Place order)
@customer_bp.route("/cart/checkout", methods=["POST"])
def checkout():
    """Place an order and clear the cart."""
    data = request.json
    user_id = data["email"]
    
    verify_user = get_customer_by_email(user_id)
    if not verify_user:
        return jsonify({"error" : "Invalid customer id"}), 404 
    customer = Customer(verify_user["name"], verify_user["email"], verify_user["password"], verify_user["order_history"], Cart(return_cart()))
    customer.checkout()

    db = "db/customer.json"
    customer_all = FileHandler.read(db)
    for i,cus in enumerate(customer_all):
        if cus["email"] == customer.get_email():
            customer_all[i]["order_history"] = customer.show_order_history()
            
    FileHandler.write(db, customer_all)

    return jsonify({"message": "Order placed successfully", "order_history": customer.show_order_history()}), 200


# View order history
@customer_bp.route("/show_order_history", methods=["GET"])
def view_orders():
    """Return all past orders for the customer."""
    data = request.json
    user_id = data["email"]
    
    verify_user = get_customer_by_email(user_id)
    if not verify_user:
        return jsonify({"error" : "Invalid customer id"}), 404 
    customer = Customer(verify_user["name"], verify_user["email"], verify_user["password"], verify_user["order_history"], Cart(return_cart()))
    return jsonify({"message": "Order history", "order_history": customer.show_order_history()}), 200
