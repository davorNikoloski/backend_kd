from Config.Config import db
from flask_login import UserMixin


# User Model
class User(db.Model):
    __tablename__ = 'user'
    u_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    sex = db.Column(db.Enum('Male', 'Female', 'Other'))
    date_birth = db.Column(db.Date)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    profile_path = db.Column(db.String(255))
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    email_confirmed = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6))
    requests_number = db.Column(db.Integer, default=0)  

    attributes = db.relationship('UserAttributes', backref=db.backref('user', lazy=True))
    friends = db.relationship('UserFriends', backref=db.backref('user', lazy=True))

# UserAttributes Model
class UserAttributes(db.Model):
    __tablename__ = 'user_attributes'
    attr_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.u_id', ondelete='CASCADE'))
    attribute_name = db.Column(db.String(50))
    attribute_value = db.Column(db.String(255))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id', ondelete='SET NULL'))

# UserFriends Model
class UserFriends(db.Model):
    __tablename__ = 'user_friends'
    uf_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.u_id', ondelete='CASCADE'))
    f_id = db.Column(db.Integer, db.ForeignKey('user.u_id', ondelete='CASCADE'))
    status = db.Column(db.Enum('pending', 'accepted', 'rejected'), nullable=False, default='pending')
    timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())

# Tag Model
class Tag(db.Model):
    __tablename__ = 'tag'
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(50), unique=True)

# Category Model
class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), unique=True)

# Post Model
class Post(db.Model):
    __tablename__ = 'post'
    p_id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.u_id', ondelete='CASCADE'))
    title = db.Column(db.String(255))
    subtitle = db.Column(db.String(255))
    content = db.Column(db.Text)
    icon_path = db.Column(db.String(255))
    image_paths = db.Column(db.Text)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id', ondelete='SET NULL'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id', ondelete='SET NULL'))
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())