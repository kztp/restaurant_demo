from models.admin import Admin
from models.staff import Staff
from models.item import Item
from flask import Blueprint, jsonify, request
from services.user_service import get_all_users
from utils.file_handler import FileHandler

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/item/promo", methods = ["POST"])
def add_promo():
    data = request.json
    admin_id = data["email"]
    menu_id = data["name"]
    menu_promo = data["promo"]
    
    admin_db = "db/admin.json"
    admin_all = get_all_users(admin_db)

    admin = None
    for user in admin_all:
        if user["email"] == admin_id:
           admin = Admin(**user)
    if not admin:
        return jsonify({"error" : "Invalid admin id"}), 404
    if not admin.add_promo(menu_id, menu_promo):
        return jsonify({"error" : "Invalid item"}), 404
    return jsonify({"message": "Adding promo code process is successful"}), 200

@admin_bp.route("/item/add", methods = ["POST"])
def add_menu():
    data = request.json
    admin_id = data["email"]
    menu_id = data["name"]
    menu_price = data["price"]
    menu_stock = data["stock"]
    
    admin_db = "db/admin.json"
    admin_all = get_all_users(admin_db)

    admin = None
    for user in admin_all:
        if user["email"] == admin_id:
           admin = Admin(**user)
    if not admin:
        return jsonify({"error" : "Invalid admin id"}), 404
    if not admin.add_menu(menu_id, menu_price, menu_stock):
        return jsonify({"error" : "Menu already exist"}), 404

    return jsonify({"message" : "Adding new menu is successful"}), 200

@admin_bp.route("/item/remove", methods = ["POST"])
def remove_menu():
    data = request.json
    admin_id = data["email"]
    menu_id = data["name"]
    
    admin_db = "db/admin.json"
    admin_all = get_all_users(admin_db)

    admin = None
    for user in admin_all:
        if user["email"] == admin_id:
           admin = Admin(**user)
    if not admin:
        return jsonify({"error" : "Invalid admin id"}), 404
    if not admin.remove_menu(menu_id):
        return jsonify({"error" : "Menu does not exist"}), 404
    return jsonify({"message" : "Selected menu is successfully removed"}), 200

@admin_bp.route("/staff/add", methods = ["POST"])
def add_staff():
    data = request.json
    admin_id = data["email1"]
    staff_id = data["name"]
    staff_email = data["email2"]
    staff_pwd = data["password"]
    
    admin_db = "db/admin.json"
    admin_all = get_all_users(admin_db)

    admin = None
    for user in admin_all:
        if user["email"] == admin_id:
           admin = Admin(**user)
    if not admin:
        return jsonify({"error" : "Invalid admin id"}), 404
    if not admin.add_staff(staff_id, staff_email, staff_pwd):
        return jsonify({"error" : "Staff already exist"}), 404

    return jsonify({"message" : "Adding new staff is successful"}), 200

@admin_bp.route("/staff/remove", methods = ["POST"])
def add_remove():
    data = request.json
    admin_id = data["email1"]
    staff_id = data["email2"]

    admin_db = "db/admin.json"
    admin_all = get_all_users(admin_db)

    admin = None
    for user in admin_all:
        if user["email"] == admin_id:
           admin = Admin(**user)
    if not admin:
        return jsonify({"error" : "Invalid admin id"}), 404
    if not admin.remove_staff(staff_id):
        return jsonify({"error" : "Staff not found"}), 404

    return jsonify({"message" : "Removing staff is successful"}), 200

@admin_bp.route("/staff/timetable/add", methods = ["POST"])
def add_timetable():
    data = request.json
    admin_id = data["email1"]
    staff_id = data["email2"]
    work_hr = data["work_hr"]

    admin_db = "db/admin.json"
    admin_all = get_all_users(admin_db)

    admin = None
    for user in admin_all:
        if user["email"] == admin_id:
           admin = Admin(**user)
    if not admin:
        return jsonify({"error" : "Invalid admin id"}), 404
    if not admin.add_timetable(staff_id, work_hr):
        return jsonify({"error" : "Staff not found"}), 404

    return jsonify({"message" : "Timetable is successfully added"}), 200
    