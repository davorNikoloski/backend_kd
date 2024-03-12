from Models.Models import User
from Config.Config import app, db
from Config.Common import custom_abort, get_user_from_jwt, convertor, get_hash_info, build_params
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import datetime, random
from flask import jsonify,Blueprint
import bcrypt

from email_validator import validate_email
#from flask_redmail import RedMail
import redmail
user_auth = Blueprint('auth', __name__)
#redmail = RedMail(app)


class Users():
    def __init__(self):
        self.table_keys = {
            "u_id": "Integer",
            "first_name": "String",
            "last_name": "String",
            "sex": "String",
            "date_birth": "Date",
            "email": "String",
            "password": "String",
            "profile_path": "String",

            "date_created": "Timestamp",
            "email_confirmed": "Boolean",
            "verification_code": "String",

            "attributes": "Relationship(UserAttributes)",
            "friends": "Relationship(UserFriends)"

        }
        pass


    def send_verification_email(self, email, verification_code):
        verification_link = f'http://yourwebsite.com/verify-email?email={email}&code={verification_code}'
        email_body = f'Click the following link to verify your email: {verification_link}\n\n' \
                    f'Or use this verification code: {verification_code}'

        try:
            redmail.send(
                receivers=email,
                subject='Verify Your Email',
                html=email_body,
                sender='pyFlaskDBTest@hotmail.com'
            )
            return True
        except Exception as e:
            print(f"Failed to send verification email to {email}: {str(e)}")
            return False


#---------------REGISTER---------------------
    def register(self, request):
        data = request.get_json()
        print(data)
        user = User()

        #-----REQUIRED DATA---------
        required = ["u_id", "first_name", "last_name", "email", "password", "verification_code"]
        for key in required:
            if key not in data:
                return custom_abort(400, "You are missing a required key - " + key)
        

        #------------------- EMAIL FORMAT CHECK----------------------
        try:
            valid_email = validate_email(data["email"])
            data["email"] = valid_email.email
        except Exception as e:
            return custom_abort(400, "Invalid email format")

        #------------------- EMAIL REGISTERED CHECK----------------------
        existing_email = Users.query.filter_by(email=data["email"]).first()
        if existing_email is not None:
            return custom_abort(409, "This Email is already registered!")
        
        hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
        verification_code = str(random.randint(100000, 999999))



        #---------SAVE THE DATA TO THE User DB---------------
        [setattr(user, key, data[key]) for key in required]
        print("hashed pw: " + hashed_password)
        user.password = hashed_password.decode("utf-8") 
        print("hashed decoded: " + hashed_password.decode("utf-8") )

        user.verification_code = verification_code
        db.session.add(user)
        db.session.commit()

        # Send verification email
        self.send_verification_email(data['email'], verification_code)

        user = User.query.filter_by(u_id=user.u_id).first()

        user_ret = convertor(user, ["password", "confirmed"])
        access_token = create_access_token(user_ret, expires_delta=datetime.timedelta(days=1))
        refresh = create_refresh_token(user_ret, expires_delta=datetime.timedelta(days=30))
        msg = "Verification email sent. Check your email for instructions."

        return jsonify({
        "user": user_ret,
        "access_token": access_token,
        "refresh": refresh,
        "msg": msg
    }), 200


    #---------------REGISTER---------------------
    def login(self, request):
        data = request.get_json()
        print(data)


        #-----REQUIRED DATA---------
        required = ["email", "password"]
        for key in required:
            if key not in data:
                return "Missing required key: " + key, 400


        user = User.query.filter_by(email=data["email"]).first()

        #------------------- EMAIL FORMAT CHECK----------------------
        try:
            valid_email = validate_email(data["email"])
            data["email"] = valid_email.email
        except Exception as e:
            return custom_abort(400, "You have entered an invalid email format!")

        if user is None or not bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")):
                    return "Invalid email or password", 401
        
        user_ret = convertor(user, ["password", "confirmed"])
        access_token = create_access_token(user_ret, expires_delta=datetime.timedelta(days=1))
        refresh = create_refresh_token(user_ret, expires_delta=datetime.timedelta(days=30))
        
        return jsonify({
        "user": user_ret,
        "access_token": access_token,
        "refresh": refresh
    }), 200





user_crud = Users()