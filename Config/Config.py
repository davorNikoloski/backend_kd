from Config.Constants import constants, SECRET_KEY
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_login import LoginManager

import os

app = Flask(__name__, template_folder='../Templates', static_url_path='/Static/React', static_folder=constants["static_root"])

#-----------------------DATABASE CONFIG----------------------
uri = "mysql+pymysql://"+constants["mysql"]["user"]+":"+constants["mysql"]["password"]+"@"+constants["mysql"]["host"]+"/"+constants["mysql"]["db_name"]+"?&autocommit=false"
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 50 MB


#------------------------JWT CONFIG----------------------------------------
app.secret_key = SECRET_KEY
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'query_string']
app.config['JWT_BLACKLIST_ENABLED'] = True

#------------------MAIL CONFIG------------------


app.config['EMAIL_HOST'] = 'smtp.office365.com'  # Correct SMTP server address for Outlook/Hotmail
app.config['EMAIL_PORT'] = 587
app.config['EMAIL_USERNAME'] = constants["email"]
app.config['EMAIL_PASSWORD'] = constants["email_pw"]
app.config['MAIL_DEFAULT_SENDER'] = constants["email"]
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


#---------------------STATIC CONFIG------------------------------------------------------------

current_directory = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = constants["static_root"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.static_folder = UPLOAD_FOLDER


#---------------DB,JWT,etc...--------------

db = SQLAlchemy(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)

CORS(app)  
#CORS(app, resources={r"/user/*": {"origins": "http://localhost:5000"}})

def build_db():
    with app.app_context():
        try:
            print('buidling db')
            # Establish a connection to the database
            db.create_all()
            # The connection is valid
            print("Connection to database is valid.")

        except Exception as e:
            # An exception was raised, indicating a problem with the connection
            print("Error: Could not establish a connection to the database.")
            print("Error message:", e)

