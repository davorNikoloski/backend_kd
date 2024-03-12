from Models.Models import UserFriends
from Config.Config import db
from Config.Common import custom_abort
from Models.Models import User
from flask import jsonify,Blueprint


user_friends_crud = Blueprint('friends', __name__)


class UserFriends():
    def __init__(self):
        self.table_keys = {
            "uf_id": "Integer",
            "u_id": "Integer",
            "f_id": "Integer",
            "status": "String",
            "timestamp": "Timestamp",
        }
        pass


#-------------------------SEND FRIEND REQUEST-----------------
    def send_friend_request(self, request):
        data = request.get_json()
        # Assuming required keys are sender_id and receiver_id
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        
        # Validate if sender and receiver exist and are not already friends
        sender = User.query.get(sender_id)
        receiver = User.query.get(receiver_id)
        if sender is None or receiver is None:
            return custom_abort(400, "Sender or receiver does not exist")
        
        if receiver in sender.friends:
            return custom_abort(400, "Friend request already sent or users are already friends")
        
        # Check if sender has exceeded the limit of rejected friend requests for the receiver
        if sender.requests_number(receiver_id) >= 3:
            return custom_abort(400, "You have reached the limit of rejected friend requests for this user")
        
        # Create a new UserFriends instance to represent the friend request
        friend_request = UserFriends(u_id=sender_id, f_id=receiver_id, status='pending')
        
        # Add and commit to the database
        db.session.add(friend_request)
        db.session.commit()
        
        return jsonify({
            "message": "Friend request sent successfully"
        }), 201




#------------------------ACCEPT FRIEND REQUEST-----------------
    def accept_friend_request(self, request):
        data = request.get_json()
        # Assuming required keys are sender_id and receiver_id
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        
        # Validate if sender and receiver exist and there's a pending friend request
        sender = User.query.get(sender_id)
        receiver = User.query.get(receiver_id)
        if sender is None or receiver is None:
            return custom_abort(400, "Sender or receiver does not exist")
        
        friend_request = UserFriends.query.filter_by(u_id=sender_id, f_id=receiver_id, status='pending').first()
        if friend_request is None:
            return custom_abort(400, "No pending friend request found")
        
        # Update friend request status to accepted
        friend_request.status = 'accepted'
        db.session.commit()
        
        # Add both users to each other's friends list
        sender.friends.append(receiver)
        receiver.friends.append(sender)
        db.session.commit()
        
        return jsonify({
            "message": "Friend request accepted successfully"
        }), 200
    


#-------------------------REJECT FRIEND REQUEST-----------------
    def reject_friend_request(self, request):
        data = request.get_json()
        # Assuming required keys are sender_id and receiver_id
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        
        sender = User.query.get(sender_id)
        receiver = User.query.get(receiver_id)
        if sender is None or receiver is None:
            return custom_abort(400, "Sender or receiver does not exist")
        
        friend_request = UserFriends.query.filter_by(u_id=sender_id, f_id=receiver_id, status='pending').first()
        if friend_request is None:
            return custom_abort(400, "No pending friend request found")
        
        friend_request.status = 'rejected'
        # Increment requests_number for the receiver
        receiver.requests_number = receiver.requests_number + 1
        db.session.commit()
        
        if receiver.requests_number >= 3:
            # Add logic to prevent sending further requests
            # For example: Disable the send_friend_request API for this user
            pass
        
        return jsonify({
            "message": "Friend request rejected successfully"
        }), 200
    
user_friend = UserFriends()