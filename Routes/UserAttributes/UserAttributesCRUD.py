from Models.Models import UserAttributes
from Config.Config import app, db
from Config.Common import custom_abort, convertor
from flask import jsonify,Blueprint

user_attributes_crud = Blueprint('user_attributes', __name__)

class UserAttributes():
    def __init__(self):
        self.table_keys = {
            "attr_id": "Integer",
            "u_id": "Integer",
            "attribute_name": "String",
            "attribute_value": "String",

            "tag_id": "Integer",
        }
        pass



    def create(self, request):
        data = request.get_json()
        
        # Check if all required keys are present
        required_keys = ["u_id", "attribute_name", "attribute_value"]
        for key in required_keys:
            if key not in data:
                return custom_abort(400, f"Missing required key: {key}")
        
        # Create a new UserAttribute instance
        user_attribute = UserAttributes(**data)
        
        # Add and commit to the database
        db.session.add(user_attribute)
        db.session.commit()
        
        return jsonify({
            "message": "User attribute created successfully",
            "user_attribute": convertor(user_attribute)
        }), 201





    def read(self, attr_id):
        user_attribute = UserAttributes.query.get(attr_id)
        if user_attribute is None:
            return custom_abort(404, "User attribute not found")
        
        return jsonify({
            "user_attribute": convertor(user_attribute)
        }), 200





    def update(self, attr_id, request):
        data = request.get_json()
        
        user_attribute = UserAttributes.query.get(attr_id)
        if user_attribute is None:
            return custom_abort(404, "User attribute not found")
        
        # Update user attribute fields
        for key, value in data.items():
            setattr(user_attribute, key, value)
        
        # Commit changes
        db.session.commit()
        
        return jsonify({
            "message": "User attribute updated successfully",
            "user_attribute": convertor(user_attribute)
        }), 200



    def delete(self, attr_id):
        user_attribute = UserAttributes.query.get(attr_id)
        if user_attribute is None:
            return custom_abort(404, "User attribute not found")
        
        db.session.delete(user_attribute)
        db.session.commit()
        
        return jsonify({
            "message": "User attribute deleted successfully"
        }), 200
    
    
user_attributes = UserAttributes()