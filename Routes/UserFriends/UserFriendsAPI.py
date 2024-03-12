from flask import Blueprint, request
from flask_jwt_extended import jwt_required

user_friends_api = Blueprint('user_friends_api', __name__)

# Import UserFriendsCRUD class
from Routes.UserFriends.UserFriendsCRUD import user_friend


@user_friends_api.route('/friend-request', methods=['POST'])
@jwt_required()
def send_friend_request():
    sender_id = request.json.get('sender_id')
    receiver_id = request.json.get('receiver_id')
    return user_friend.send_friend_request(sender_id, receiver_id)




@user_friends_api.route('/friend-request/accept', methods=['POST'])
@jwt_required()
def accept_friend_request():
    sender_id = request.json.get('sender_id')
    receiver_id = request.json.get('receiver_id')
    return user_friend.accept_friend_request(sender_id, receiver_id)




@user_friends_api.route('/friend-request/reject', methods=['POST'])
@jwt_required()
def reject_friend_request():
    sender_id = request.json.get('sender_id')
    receiver_id = request.json.get('receiver_id')
    return user_friend.reject_friend_request(sender_id, receiver_id)