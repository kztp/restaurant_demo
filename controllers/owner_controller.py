from models.owner import Owner
from flask import Blueprint, jsonify, request
from services.user_service import get_all_users

owner_bp = Blueprint("owner", __name__)

@owner_bp.route("/sale",methods=["GET"])
def show_sale():
    data = request.json
    user_id = data["email"]
    
    user_db = "db/owner.json"
    users = get_all_users(user_db)
    
    owner = None
    for user in users:
        if user["email"] == user_id:
           owner = Owner(**user)
    if not owner:
        return jsonify({"error" : "Invalid owner id"}), 404

    return jsonify({"data" : owner.show_sales() }), 200

@owner_bp.route("/staff", methods=["GET"])
def show_staff():
    data = request.json
    user_id = data["email"]
    
    user_db = "db/owner.json"
    users = get_all_users(user_db)
    
    owner = None
    for user in users:
        if user["email"] == user_id:
           owner = Owner(**user)
    if not owner:
        return jsonify({"error" : "Invalid owner id"}), 404

    return jsonify({"data" : owner.show_staffs() }), 200
