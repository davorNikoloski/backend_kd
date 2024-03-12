from Models.Models import Tag
from Config.Config import app, db
from Config.Common import custom_abort
from flask import jsonify,Blueprint

tags_crud = Blueprint('tags', __name__)

class Tags():
    def __init__(self):
        self.table_keys = {
            "tag_id": "Integer",
            "tag_name": "String",
        }
        pass

    def create(self, request):
        data = request.get_json()
        tag_name = data.get('tag_name')
        
        # Check if tag_name is provided
        if not tag_name:
            return custom_abort(400, "Tag name is required")
        
        # Check if tag_name already exists
        existing_tag = Tag.query.filter_by(tag_name=tag_name).first()
        if existing_tag:
            return custom_abort(400, "Tag with this name already exists")
        
        # Create a new Tag instance
        new_tag = Tag(tag_name=tag_name)
        
        # Add and commit to the database
        db.session.add(new_tag)
        db.session.commit()
        
        return jsonify({
            "message": "Tag created successfully",
            "tag": {
                "tag_id": new_tag.tag_id,
                "tag_name": new_tag.tag_name
            }
        }), 201
    
    def read(self, tag_id):
        tag = Tag.query.get(tag_id)
        if not tag:
            return custom_abort(404, "Tag not found")
        
        return jsonify({
            "tag": {
                "tag_id": tag.tag_id,
                "tag_name": tag.tag_name
            }
        }), 200
    
    def update(self, tag_id, request):
        data = request.get_json()
        tag_name = data.get('tag_name')
        
        tag = Tag.query.get(tag_id)
        if not tag:
            return custom_abort(404, "Tag not found")
        
        # Update tag_name if provided
        if tag_name:
            tag.tag_name = tag_name
        
        # Commit changes
        db.session.commit()
        
        return jsonify({
            "message": "Tag updated successfully",
            "tag": {
                "tag_id": tag.tag_id,
                "tag_name": tag.tag_name
            }
        }), 200
    
    def delete(self, tag_id):
        tag = Tag.query.get(tag_id)
        if not tag:
            return custom_abort(404, "Tag not found")
        
        # Delete the tag
        db.session.delete(tag)
        db.session.commit()
        
        return jsonify({
            "message": "Tag deleted successfully"
        }), 200
    

tags = Tags()
