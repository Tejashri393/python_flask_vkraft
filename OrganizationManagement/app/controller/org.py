
from flask import Blueprint, request, jsonify
from app.Model.org import Organisation, db
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
import logging

org_bp = Blueprint('organisation', __name__)

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Helper function for validation
def validate_organisation_data(data, required_fields):
    """Validates the organisation data."""
    for field in required_fields:
        if field not in data or not data[field]:  # Checks if the field is missing or empty
            return False, f"The field '{field}' is required and cannot be empty."
    return True, None

# Route to get all organisations
@org_bp.route('/organisations', methods=['GET'])
def get_all_organisations():
    organisations = Organisation.query.all()
    if not organisations:
        return jsonify({"message": "No organisations found in the database."}), 404
    return jsonify([org.to_dict() for org in organisations]), 200

# Route to get an organisation by code
@org_bp.route('/organisation/<int:code>', methods=['GET'])
def get_organisation_by_code(code):
    try:
        organisation = Organisation.query.get_or_404(code)
        return jsonify(organisation.to_dict()), 200
    except NotFound:
        return jsonify({"message": "Organisation not found"}), 404

# Route to add a new organisation
@org_bp.route('/organisation', methods=['POST'])
def add_organisation():
    data = request.get_json()

    # Validate required fields
    required_fields = ['code', 'org_name', 'details']
    is_valid, error_message = validate_organisation_data(data, required_fields)
    if not is_valid:
        return jsonify({"message": error_message}), 400

    new_organisation = Organisation(
       

        code=data['code'],
        org_name=data['org_name'],
        details=data['details'],
        
    )

    try:
        db.session.add(new_organisation)
        db.session.commit()
        return jsonify(new_organisation.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"IntegrityError: {str(e)}")
        return jsonify({"message": "Integrity error occurred. Please check your data."}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500

# Route to edit an organisation
@org_bp.route('/organisation/<int:code>', methods=['PUT'])
def edit_organisation(code):
    data = request.get_json()
    try:
        organisation = Organisation.query.get_or_404(code)

        # Update organisation details
        for key, value in data.items():
            if hasattr(organisation, key):
                setattr(organisation, key, value)

        db.session.commit()
        return jsonify(organisation.to_dict()), 200
    except NotFound:
        return jsonify({"message": "Organisation not found"}), 404
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500

# Route to delete an organisation
@org_bp.route('/organisation/<int:code>', methods=['DELETE'])
def delete_organisation(code):
    try:
        organisation = Organisation.query.get_or_404(code)
        db.session.delete(organisation)
        db.session.commit()
        return jsonify({"message": "Organisation deleted successfully"}), 200
    except NotFound:
        return jsonify({"message": "Organisation not found"}), 404
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500


# Route to get an organisation by org_name
@org_bp.route('/organisation/name/<string:org_name>', methods=['GET'])
def get_organisation_by_name(org_name):
    try:
        organisation = Organisation.query.filter_by(org_name=org_name).first()
        if not organisation:
            return jsonify({"message": "Organisation not found"}), 404
        return jsonify(organisation.to_dict()), 200
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"message": "An unexpected error occurred.", "details": str(e)}), 500
