from datetime import datetime
import json
import os
from db import db
from db import User, Message
from flask import Flask
from flask import request

app = Flask(__name__)
db_filename = "tchat.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats


def success_response(data, code=200):
    return json.dumps({"success": True, "data": data}), code


def failure_response(message, code=404):
    return json.dumps({"success": False, "error": message}), code


# -- USER ROUTES ---------------------------------------------------


# Add user
@app.route("/api/users/", methods=["POST"])
def create_user():
    body = json.loads(request.data)
    body_name = body.get('name')
    if body_name is None:
        return failure_response("Please provide a name", 400)
    new_user = User(name=body_name)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)


# Get User
@app.route("/api/users/<int:user_id>/")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response('User not found!')
    return success_response(user.serialize())


# Delete user
@app.route("/api/users/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response('User not found!')
    user_data = user.serialize()
    db.session.delete(user)
    db.session.commit()
    return success_response(user_data)


# Get all users
@app.route("/api/users/")
def get_all_users():
    users = User.query.all()
    if users is None:
        return success_response([])
    return success_response([user.serialize() for user in users])


# -- MESSAGE ROUTES ---------------------------------------------------


# Send message
@app.route("/api/messages/", methods=["POST"])
def send_message():
    body = json.loads(request.data)
    body_content = body.get('content')
    date = datetime.now()
    read = False
    body_sender_id = body.get('sender_id')
    body_receiver_id = body.get('receiver_id')
    if body_content is None or body_sender_id is None:
        return failure_response("Please provide a content and sender_id", 400)
    if User.query.filter_by(id=body_sender_id).first() is None:
        return failure_response("Sender not found")
    if User.query.filter_by(id=body_receiver_id).first() is None:
        return failure_response("Receiver not found")
    new_message = Message(
        content=body_content,
        date=date,
        read=read,
        sender_id=body_sender_id,
        receiver_id=body_receiver_id
    )
    db.session.add(new_message)
    db.session.commit()
    return success_response(new_message.serialize(), 201)

# Get all messages
@app.route("/api/users/<int:user_id>/messages/")
def get_all_messages(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found")
    unread_only = request.args.get('unread') != None
    if unread_only:
        messages = user.get_unread_messages()
        for message in messages:
            message.read = True
        db.session.commit()
    else:
        messages = user.get_all_messages()
    return success_response([message.serialize() for message in messages])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("DEBUG", False)
    app.run(host="0.0.0.0", port=port, debug=debug)
