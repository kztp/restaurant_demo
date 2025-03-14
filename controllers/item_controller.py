from flask import Blueprint, jsonify, request
from models.item import Item

item_bp = Blueprint("item", __name__)


# Get all items
@item_bp.route("/items", methods=["GET"])
def get_all_items():

    """Return all items from the JSON file."""

    items = Item.load_items()
    return jsonify([item.to_dict() for item in items])


# Get a single item by ID
@item_bp.route("/items/<item_id>", methods=["GET"])
def get_item(item_id):
    
    """Return a single item by ID."""
    
    items = Item.load_items()
    item = next((i for i in items if i.item_id == item_id), None)
    if item:
        return jsonify(item.to_dict())
    return jsonify({"error": "Item not found"}), 404


# Update stock for an item
@item_bp.route("/items/<item_id>/update_stock", methods=["POST"])
def update_stock(item_id):
    
    """Update stock for an item."""
    
    data = request.json
    quantity = data.get("quantity", 0)  # Get quantity from request
    
    # Ensure quantity is a valid integer
    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"error": "Invalid quantity"}), 400
    
    if quantity <= 0:
        return jsonify({"error": "Quantity must be positive"}), 400

    # Load items from storage 
    items = Item.load_items()
    item = next((i for i in items if i.item_id == item_id), None)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Update stock
    item.stock += quantity  # Increase stock
    Item.save_items(items)  # Save updated items back to storage

    return jsonify({"message": "Stock updated", "item": item.to_dict()})


# Filter items by name or price range
@item_bp.route("/items/filter", methods=["GET"])
def filter_items():
    
    """Filter items by name or price range."""
    
    items = Item.load_items()  

    if not items:
        return jsonify({"error": "No items found"}), 404  # Handle empty items list

    # Get query parameters
    name_query = request.args.get("name", "").strip().lower()
    min_price = request.args.get("min_price", 0)
    max_price = request.args.get("max_price", float("inf"))

    # Convert price filters to float safely
    try:
        min_price = float(min_price)
        max_price = float(max_price)
    except ValueError:
        return jsonify({"error": "Invalid price range"}), 400  # Handle incorrect price inputs

    # Debugging: Print incoming values
    print(f"Filtering items by name: '{name_query}', price range: {min_price} - {max_price}")

    # Apply filtering conditions
    filtered_items = [
        item for item in items
        if (not name_query or name_query in item.name.lower())  # Name filter
        and (min_price <= float(item.price) <= max_price)  # Price range filter
    ]

    if not filtered_items:
        return jsonify({"message": "No items match the filters"}), 404  # Handle no matches

    return jsonify([item.to_dict() for item in filtered_items])


# Add a new item
@item_bp.route("/items", methods=["POST"])
def add_item():
    """Add a new item."""
    data = request.json

    # Extract data with default values
    item_id = data.get("item_id")
    name = data.get("name", "").strip()
    price = data.get("price", 0)
    stock = data.get("stock", 0)

    # Validate required fields
    if not item_id or not name or float(price) <= 0 or int(stock) < 0:
        return jsonify({"error": "Invalid item data"}), 400

    items = Item.load_items()
    
    # Check if item ID already exists
    if any(item.item_id == item_id for item in items):
        return jsonify({"error": "Item ID already exists"}), 400

    # Create new item and save
    new_item = Item(item_id, name, float(price), int(stock))
    items.append(new_item)
    Item.save_items(items)

    return jsonify({"message": "Item added", "item": new_item.to_dict()}), 201


# Delete an item by ID
@item_bp.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Delete an item by ID."""
    items = Item.load_items()
    
    # Find the item
    item = next((i for i in items if i.item_id == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    # Remove item from list and save
    items = [i for i in items if i.item_id != item_id]
    Item.save_items(items)

    return jsonify({"message": "Item deleted"}), 200