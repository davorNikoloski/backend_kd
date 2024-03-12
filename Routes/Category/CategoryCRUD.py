from Models.Models import Category
from Config.Config import app, db
from Config.Common import custom_abort
from flask import jsonify,Blueprint

categories_crud = Blueprint('categories', __name__)

class Categories():
    def __init__(self):
        self.table_keys = {
            "category_id": "Integer",
            "category_name": "String",
        }
        pass

    def create(self, request):
        data = request.get_json()
        category_name = data.get('category_name')
        
        # Check if category_name is provided
        if not category_name:
            return custom_abort(400, "Category name is required")
        
        # Check if category_name already exists
        existing_Category = Category.query.filter_by(category_name=category_name).first()
        if existing_Category:
            return custom_abort(400, "Category with this name already exists")
        
        # Create a new Category instance
        new_Category = Category(category_name=category_name)
        
        # Add and commit to the database
        db.session.add(new_Category)
        db.session.commit()
        
        return jsonify({
            "message": "Category created successfully",
            "Category": {
                "category_id": new_Category.category_id,
                "category_name": new_Category.category_name
            }
        }), 201
    
    def read(self, category_id):
        Category = Category.query.get(category_id)
        if not Category:
            return custom_abort(404, "Category not found")
        
        return jsonify({
            "Category": {
                "category_id": Category.category_id,
                "category_name": Category.category_name
            }
        }), 200
    
    def update(self, category_id, request):
        data = request.get_json()
        category_name = data.get('category_name')
        
        Category = Category.query.get(category_id)
        if not Category:
            return custom_abort(404, "Category not found")
        
        # Update category_name if provided
        if category_name:
            Category.category_name = category_name
        
        # Commit changes
        db.session.commit()
        
        return jsonify({
            "message": "Category updated successfully",
            "Category": {
                "category_id": Category.category_id,
                "category_name": Category.category_name
            }
        }), 200
    
    def delete(self, category_id):
        Category = Category.query.get(category_id)
        if not Category:
            return custom_abort(404, "Category not found")
        
        # Delete the Category
        db.session.delete(Category)
        db.session.commit()
        
        return jsonify({
            "message": "Category deleted successfully"
        }), 200
    

categories = Categories()
