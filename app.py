from Config.Config import app, db

from Routes.User.UserAPI import user_api

#------------------ CONNECTION TO THE DB ---------------------------
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


#------------------BLUEPRINTS / ROUTES ----------------------------

app.register_blueprint(user_api, url_prefix='/user')





#---------------------RUN APP --------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) 