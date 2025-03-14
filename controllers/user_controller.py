from flask import Blueprint, request, jsonify
from models.user import User, Customer, Staff, Administrator, Owner

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def add_user():
    data = request.json
    user_type = data.get('role')

    # dynamically create user object based on role
    if user_type == 'customer':
        user = Customer(data['user_id'], data['name'], data['email'], data['password'])
    elif user_type == 'staff':
        user = Staff(data['user_id'], data['name'], data['email'], data['password'])
    elif user_type == 'administrator':
        user = Administrator(data['user_id'], data['name'], data['email'], data['password'])
    elif user_type == 'owner':
        user = Owner(data['user_id'], data['name'], data['email'], data['password'])
    else:
        return jsonify({"error": "Invalid role"}), 400

    User.add_user(user)
    return jsonify({"message": f"{user_type.capitalize()} added successfully"}), 201


@user_bp.route('/users/<role>', methods=['GET'])
def get_users_by_role(role):
    if role not in ['customer', 'staff', 'administrator', 'owner']:
        return jsonify({"error": "Invalid role"}), 400
    return jsonify(User.get_all_users(role))