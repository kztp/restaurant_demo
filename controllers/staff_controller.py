from flask import Blueprint, jsonify, request
from services.user_service import get_all_users
from models.staff import Staff
from models.item import Item
from utils.file_handler import FileHandler

staff_bp = Blueprint("staff", __name__)


@staff_bp.route("/doorder", methods=["GET"])
def do_order():
    """change the status of order and transfer to complete order file"""
    data = request.json
    user_id = data["email"]
    
    user_db = "db/staff.json"
    users = get_all_users(user_db)

    staff = None
    for user in users:
        if user["email"] == user_id:
           staff = Staff(**user)
    if not staff:
        return jsonify({"error" : "Invalid staff id"}), 404

    staff.do_order()
    return jsonify({"message": "One order is accomplished"}), 200


@staff_bp.route("/table/add", methods=["POST"])
def add_table():
    """change table status : from occupied to avaliable"""
    data = request.json
    staff_id = data["email"]
    table_id = data["table"]

    staff_db = "db/staff.json"

    staff = None
    staff_all = get_all_users(staff_db)
    for user in staff_all:
        if user["email"] == staff_id:
           staff = Staff(**user)
    if not staff:
        return jsonify({"error" : "Invalid staff id"}), 404

    if not staff.manage_table(table_id, "avaliable"):
        return jsonify({"message" : "Selected table is already avaliable"}), 400
    
    return jsonify({"message": "Adding process is successful"}), 200


@staff_bp.route("/table/reserve", methods=["POST"])
def reserve_table():
    """change table status : from avaliable to occupied"""
    data = request.json
    staff_id = data["email"]
    table_id = data["table"]

    staff_db = "db/staff.json"

    staff = None
    staff_all = get_all_users(staff_db)
    for user in staff_all:
        if user["email"] == staff_id:
           staff = Staff(**user)
    if not staff:
        return jsonify({"error" : "Invalid staff id"}), 404

    if not staff.manage_table(table_id, "reserved"):
        return jsonify({"message" : "Selected table is already reserved"}), 400
    
    return jsonify({"message": "Reserving process is successful"}), 200


@staff_bp.route("/show_timetable", methods=["GET"])
def show_timetable():
    """view the timetable of staff"""
    data = request.json
    staff_id = data["email"]
    
    staff_db = "db/staff.json"
    staff_all = get_all_users(staff_db)

    staff = None
    for user in staff_all:
        if user["email"] == staff_id:
           staff = Staff(**user)
    if not staff:
        return jsonify({"error" : "Invalid staff id"}), 404
    
    return jsonify({"message" : "Getting timetable is successful", "data" : staff.show_timetable()}), 200
    

@staff_bp.route("/item/add", methods = ["POST"])
def add_stock():
    """Increase the stock of Menu"""
    data = request.json
    staff_id = data["email"]
    menu_id = data["name"]
    menu_quantity = data["quantity"]
    
    staff_db = "db/staff.json"
    menu_db = "db/menu.json"
    menu_all = FileHandler.read(menu_db)
    staff_all = get_all_users(staff_db)

    staff = None
    for user in staff_all:
        if user["email"] == staff_id:
           staff = Staff(**user)
    if not staff:
        return jsonify({"error" : "Invalid staff id"}), 404
    
    item = None
    for menu in menu_all:
        if menu["name"] == menu_id:
            item = Item(**menu)        
    if not item:
        return jsonify({"error" : "Invalid item"}), 404
    staff.add_stock(item, menu_quantity)
    
    for index, menu in enumerate(menu_all):
        if menu["name"] == menu_id:
            menu_all[index] = item.to_dict()
    FileHandler.write(menu_db, menu_all)

    return jsonify({"message" : "Adding stock is successful"}), 200
