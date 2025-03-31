from flask import Blueprint, request, jsonify, session
from models.customer import Customer
from models.owner import Owner
from models.admin import Admin
from models.staff import Staff
from services.user_service import get_all_users,get_customer_by_email, register_customer

auth_bp = Blueprint('user', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data["email"]

    user = get_customer_by_email(email)
    if user:
        return jsonify({"message" : f"user already exits. Please change the email"}), 400
    
    new_customer = Customer(**data)
    register_customer(new_customer.to_dict())

    return jsonify({"message" : f"Registration successful"}), 201
    

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    role = data["role"]
    email = data["email"]
    pwd = data["password"]
   
    db = None
    if role == "owner":
        db = "db/owner.json"
    elif role == "admin":
        db = "db/admin.json"
    elif role == "staff":
        db = "db/staff.json"
    else:
        db = "db/customer.json"
    
    users = get_all_users(db)
    verified_user = None
    for user in users:
        if user["email"] == email:
            if role == "owner":
                verified_user = Owner(**user)
            elif role == "admin":
                verified_user = Admin(**user)
            elif role == "staff":
                verified_user = Staff(**user)
            elif role == "customer":
                verified_user = Customer(**user)
    
    if not verified_user:
        return jsonify({"message" : "User do not exit"}), 401

    if not verified_user.verify_password(pwd):
        return jsonify({"message" : "Invalid password"}), 401
    return jsonify({"message" : "Login successful",
                    "data" : {
                      "email" :  verified_user.get_email()
                    }
                    }) ,200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Successfully logged out"}), 200