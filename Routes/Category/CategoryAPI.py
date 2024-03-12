from flask import jsonify, Blueprint, request
from Config.Config import app, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from Config.Common import crud_routes, custom_abort

from Routes.Category.CategoryCRUD import categories
from Models.Models import Category

categories_api = Blueprint('categories_api', __name__)

# API endpoints
@categories_api.route('/tag', methods=['POST'])
@jwt_required()
def create_tag():
    return categories.create(request)

@categories_api.route('/tag/<int:tag_id>', methods=['GET'])
@jwt_required()
def get_tag(tag_id):
    return categories.read(tag_id)

@categories_api.route('/tag/<int:tag_id>', methods=['PUT'])
@jwt_required()
def update_tag(tag_id):
    return categories.update(tag_id, request)

@categories_api.route('/tag/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def delete_tag(tag_id):
    return categories.delete(tag_id)