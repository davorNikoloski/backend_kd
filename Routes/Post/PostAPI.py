from flask import request
from flask import Blueprint, render_template, request, jsonify,redirect, url_for
from Config.Config import app, db, login_manager
from flask import render_template_string
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request

from Config.Common import crud_routes, custom_abort
from Routes.Post.PostCRUD import posts
from Models.Models import Post



posts_api = Blueprint('post', __name__)


@posts_api.route('/create', methods=['POST'])
@jwt_required()
def create_post():
    return posts.create(request)



@posts_api.route('/read/<int:post_id>', methods=['GET'])
def get_post(post_id):
    return posts.read(post_id)



@posts_api.route('/update/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    return posts.update(post_id, request)



@posts_api.route('/delete/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    return posts.delete(post_id)
