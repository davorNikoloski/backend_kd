from flask import jsonify, Blueprint, request
from Config.Config import app, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from Config.Common import crud_routes, custom_abort

from Routes.UserAttributes.UserAttributesCRUD import user_attributes
from Models.Models import UserAttributes

user_attributes_api = Blueprint('user_attributes_api', __name__)


#-----------------CREATE------------------
@user_attributes_api.route('/user-attributes', methods=['POST'])
def create():
    return user_attributes.create(request)


#-----------------READ------------------
@user_attributes_api.route('/user-attributes/<int:attr_id>', methods=['GET'])
def read(attr_id):
    return user_attributes.read(attr_id)


#-----------------UPDATE------------------
@user_attributes_api.route('/user-attributes/<int:attr_id>', methods=['PUT'])
@jwt_required()
def update(attr_id):
    return user_attributes.update(attr_id, request)


#-----------------DELETE------------------
@user_attributes_api.route('/user-attributes/<int:attr_id>', methods=['DELETE'])
@jwt_required()
def delete(attr_id):
    return user_attributes.delete(attr_id)