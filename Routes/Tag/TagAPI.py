from flask import jsonify, Blueprint, request
from Config.Config import app, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from Config.Common import crud_routes, custom_abort

from Routes.Tag.TagCRUD import tags
from Models.Models import Tag

tags_api = Blueprint('tags_api', __name__)

# API endpoints
@tags_api.route('/tag', methods=['POST'])
@jwt_required()
def create_tag():
    return tags.create(request)

@tags_api.route('/tag/<int:tag_id>', methods=['GET'])
@jwt_required()
def get_tag(tag_id):
    return tags.read(tag_id)

@tags_api.route('/tag/<int:tag_id>', methods=['PUT'])
@jwt_required()
def update_tag(tag_id):
    return tags.update(tag_id, request)

@tags_api.route('/tag/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def delete_tag(tag_id):
    return tags.delete(tag_id)