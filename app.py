from Config.Config import app, db

from Routes.User.UserAPI import user_api
from Routes.UserAttributes.UserAttributesAPI import user_attributes_api 
from Routes.UserFriends.UserFriendsAPI import user_friends_api
from Routes.Category.CategoryAPI import categories_api
from Routes.Tag.TagAPI import tags_api
from Routes.Post.PostAPI import posts_api





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
app.register_blueprint(user_attributes_api, url_prefix='/user_attr')
app.register_blueprint(user_friends_api, url_prefix='/user_frnd')
app.register_blueprint(categories_api, url_prefix='/category')
app.register_blueprint(tags_api, url_prefix='/tag')
app.register_blueprint(posts_api, url_prefix='/post')



#---------------------RUN APP --------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) 