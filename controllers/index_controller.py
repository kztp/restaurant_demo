from flask import Blueprint, jsonify
from services.menu_service import get_all_menu
index_bp = Blueprint("index", __name__)

@index_bp.route('/', methods = ['GET'])
def index():
    # fetch all menu 
    menu_data = get_all_menu()
    return jsonify({
        "message" : "Welcome to Restaurant",
        "status" : "running",
        "menu" : menu_data
    }), 200