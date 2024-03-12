from flask import Blueprint, render_template, request, jsonify,redirect, url_for
from Config.Config import app, db, login_manager
from flask import render_template_string
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request

from Config.Common import crud_routes, custom_abort
from Routes.User.UserCRUD import user_crud
from Models.Models import User

user_api = Blueprint('user', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#-----------REGISTER API --------------
@user_api.route('/register', methods=["GET", "POST"])
def register():
    #print('da')

    if request.method == "POST":
        response, status_code = user_crud.register(request)
        print('da')
        if status_code == 200:
            return jsonify(response), status_code
        else:
            error_message = response
            return error_message
    return render_template('register.html')

#-----------LOGIN API --------------
@user_api.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        response, status_code = user_crud.login(request)
        if status_code == 200:
            user_data = response.get_json()['user']
            access_token = create_access_token(identity=user_data)
            user_data['access_token'] = access_token
            return jsonify(user_data), status_code
        else:
            error_message = response
            return error_message
        


@user_api.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    return user_crud.update_user(user_id, request)

@user_api.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    return user_crud.delete_user(user_id)



#-----------VERIFY EMAIL API --------------

@user_api.route('/verify', methods=["GET"])
def render_verify_email():
    current_user = get_jwt_identity()

    return jsonify(current_user)



@user_api.route('/verify-email', methods=['POST'])
@jwt_required()
def verify_email():
    data = request.get_json()
    if not data:
        return custom_abort(400, "Request body is empty or not in JSON format")

    email = data.get('email')
    verification_code = data.get('verification_code')

    user = User.query.filter_by(email=email, verification_code=verification_code).first()
    if user:
        user.email_confirmed = True
        db.session.commit()
        return jsonify({"msg": "Email verification successful"}), 200
    else:
        return custom_abort(400, "Invalid verification code")

    