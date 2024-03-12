from Models.Models import Post, Category, Tag
from Config.Config import app, db
from Config.Common import custom_abort, get_user_from_jwt, convertor, get_hash_info, build_params
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask import jsonify,Blueprint

#from flask_redmail import RedMail
import redmail
posts_crud = Blueprint('posts', __name__)

class Posts():
    def __init__(self):
        self.table_keys = {
            "p_id": "Integer",
            "u_id": "Integer",
            "title": "String",
            "subtitle": "String",
            "content": "String",
            "icon_path": "String",
            "image_paths": "String",
            "category_id": "Integer",
            "tag_id": "Integer",
            "date_created": "Timestamp"
        }
        pass


    def create(self, request):
        data = request.get_json()
                #request.form
        print(data)


        category_id = request.form.get('category_id')
        tag_id = request.form.get('tag_id')

        post = Post()


        required = ["u_id", "title", "subtitle", "content", "category_id", "tag_id"]
        for key in required:
            if key not in data:
                return custom_abort(400, "You are missing a required key - " + key)
            


        category = Category.query.get(category_id)
        if not category:
            return custom_abort(404, "Category not found")

        tag = Tag.query.get(tag_id)
        if not tag:
            return custom_abort(404, "Tag not found")
        

        [setattr(post, key, data[key]) for key in required]
        db.session.add(post)
        db.session.commit()

        return jsonify({
            "message": "Post created successfully",
            "post": convertor(post)
        }), 201
    







    def read(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return custom_abort(404, "Post not found")

        return jsonify({
            "post": convertor(post)
        }), 200





    def update(self, post_id, request):
        data = request.get_json()
        post = Post.query.get(post_id)
        if not post:
            return custom_abort(404, "Post not found")

        required = ["u_id", "title", "subtitle", "content", "category_id", "tag_id"]
        for key in required:
            if key not in data:
                return custom_abort(400, "You are missing a required key - " + key)

        category_id = request.form.get('category_id')
        tag_id = request.form.get('tag_id')

        category = Category.query.get(category_id)
        if not category:
            return custom_abort(404, "Category not found")

        tag = Tag.query.get(tag_id)
        if not tag:
            return custom_abort(404, "Tag not found")

        [setattr(post, key, data[key]) for key in required]
        db.session.commit()

        return jsonify({
            "message": "Post updated successfully",
            "post": convertor(post)
        }), 200







    def delete(self, post_id):
        post = Post.query.get(post_id)
        if not post:
            return custom_abort(404, "Post not found")

        db.session.delete(post)
        db.session.commit()

        return jsonify({
            "message": "Post deleted successfully"
        }), 200
    

posts = Posts()