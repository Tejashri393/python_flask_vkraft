from flask import Blueprint, request, jsonify
from app.Model.user import db, User
from werkzeug.exceptions import NotFound   #provided exception used requested resource is not found
from sqlalchemy.exc import IntegrityError   #exception raised by SQLAlchemy  when insert duplicate values into a column with a UNIQUE constraint
from psycopg2.errors import UniqueViolation #specific exception class from the psycopg2 library while insert duplicate values

user_bp = Blueprint('user', __name__)


#insert a new user
@user_bp.route('/users', methods=['POST'])
def add_user():
    data = request.json  # Extracts the JSON data sent in the request body
    new_user = User(  # Creates a new user object with the data provided
        fname=data['fname'],
        lname=data['lname'],
        email=data['email'],
        gender=data.get('gender'),
        contact_info=data.get('contact_info'),
        address=data.get('address'),
        mobile_no=data['mobile_no']
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User added successfully"}), 201
    except IntegrityError as e:
        db.session.rollback()  # Roll back the transaction to maintain database integrity

        # Handle duplicate field errors
        if isinstance(e.orig, UniqueViolation):
            if 'email' in str(e.orig):
                return jsonify({"message": "A user with this email already exists."}), 400
            if 'mobile_no' in str(e.orig):
                return jsonify({"message": "A user with this mobile number already exists."}), 400
        
        # Generic error message
        return jsonify({"message": "Integrity error occurred. Please check your data."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500
    
   
#get all users
@user_bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    if not users:
        return jsonify({"message": "No users found in the database."}), 404
    result = [user.to_dict() for user in users]
    return jsonify(result), 200



#get user by userId
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict()), 200
    except NotFound:
        return jsonify({"message": "This User is not present"}), 404
    



#Update User
@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.json
        
        # Update the user's details
        user.fname = data['fname']
        user.lname = data['lname']
        user.email = data['email']
        user.gender = data.get('gender')
        user.contact_info = data.get('contact_info')
        user.address = data.get('address')
        user.mobile_no = data['mobile_no']
        
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except NotFound:
        return jsonify({"message": "This User is not present"}), 404

#delete User
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except NotFound:
        return jsonify({"message": "This User is not present"}), 404