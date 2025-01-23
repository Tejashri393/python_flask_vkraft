

from flask import Blueprint, request, jsonify
from app.Model.emp import Employee, db
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
import logging

employee_bp = Blueprint('employee', __name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)


# Helper function for validation
def validate_employee_data(data, required_fields):
    """Validates the employee data."""
    for field in required_fields:
        if field not in data or not data[field]:  # Checks if the field is missing or empty
            return False, f"The field '{field}' is required and cannot be empty."
    return True, None


# Route to get all employees
@employee_bp.route('/employees', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    if not employees:
        return jsonify({"message": "No employees found in the database."}), 404
    return jsonify([employee.to_dict() for employee in employees]), 200


# Route to get an employee by ID
# @employee_bp.route('/employee/<int:emp_id>', methods=['GET'])
# def get_employee_by_id(emp_id):
#     try:

#         employee = Employee.query.get(emp_id)
#         if not employee:
#              return jsonify({"message": "No employees found in the database."})


#         return jsonify(employee.to_dict()), 200
#     except Exception as e:
#         return jsonify(str(e))


@employee_bp.route('/employee/<int:emp_id>', methods=['GET'])
def get_employee_by_id(emp_id):
    try:
        # Using filter to query by employee ID
        employee = Employee.query.filter(Employee.id == emp_id).first()
        if not employee:
            return jsonify({"message": "No employee found with the given ID."}), 404
        
        # Assuming Employee has a method to serialize data
        return jsonify(employee.to_dict()), 200
    except Exception as e:
        return jsonify({"message": "An error occurred while processing the request.", "error": str(e)}), 500



# Route to get employees by organization code
@employee_bp.route('/employees/org/<int:org_code>', methods=['GET'])
def get_employees_by_org_code(org_code):
    employees = Employee.query.filter_by(org_code=org_code).all()
    if not employees:
        return jsonify({"message": "No employees found for the given organization code."}), 404
    return jsonify([employee.to_dict() for employee in employees]), 200


# Route to add a new employee
@employee_bp.route('/employee', methods=['POST'])
def add_employee():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['fname', 'lname', 'email', 'org_code']
    is_valid, error_message = validate_employee_data(data, required_fields)
    if not is_valid:
        return jsonify({"message": error_message}), 400
    
    new_employee = Employee(
        fname=data['fname'],
        lname=data['lname'],
        email=data['email'],
        address=data.get('address'),
        org_code=data['org_code']
    )
    
    try:
        db.session.add(new_employee)
        db.session.commit()
        return jsonify(new_employee.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"IntegrityError: {str(e)}")
        return jsonify({"message": "Integrity error occurred. Please check your data."}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500


# Route to edit an employee
@employee_bp.route('/employee/<int:emp_id>', methods=['PUT'])
def edit_employee(emp_id):
    data = request.get_json()
    try:
        employee = Employee.query.get_or_404(emp_id)
        
        # Update employee details
        for key, value in data.items():
            if hasattr(employee, key):
                setattr(employee, key, value)
        
        db.session.commit()
        return jsonify(employee.to_dict()), 200
    except NotFound:
        return jsonify({"message": "Employee not found"}), 404
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500


# Route to delete an employee
@employee_bp.route('/employee/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    try:
        employee = Employee.query.get_or_404(emp_id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({"message": "Employee deleted successfully"}), 200
    except NotFound:
        return jsonify({"message": "Employee not found"}), 404
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500




@employee_bp.route('/employee/search', methods=['GET'])
def get_employee_by_fname():
    try:
        # Get 'fname' parameter from the query string
        fname = request.args.get('fname')
        
        # Validate if 'fname' is provided
        if not fname:
            return jsonify({"message": "Please provide a 'fname' query parameter."}), 400
        
        # Query for employees matching the provided first name
        employees = Employee.query.filter_by(fname=fname).all()
        
        # Check if any employees were found
        if not employees:
            return jsonify({"message": f"No employees found with fname '{fname}'."}), 404
        
        # Return all matching employees as a list of dictionaries
        return jsonify([employee.to_dict() for employee in employees]), 200
    except Exception as e:
        # Handle exceptions and return an error message
        return jsonify({"error": str(e)}), 500



