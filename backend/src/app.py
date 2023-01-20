from datetime import datetime
import json
import os
from db import db
from db import User, Message
from flask import Flask
from flask import request

app = Flask(__name__)
db_filename = "cms.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

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
    new_message = Message(
        content=body_content,
        date=date,
        read=read,
        sender_id=body_sender_id
    )
    db.session.add(new_message)
    db.session.commit()
    return success_response(new_message.serialize(), 201)

# Get unread messages
@app.route("/api/users/<int:user_id>/messages/unread/")
def get_unread_messages(user_id):
    messages = Message.query.filter_by(receiver_id=user_id, read=False).all()
    if messages is None:
        return failure_response('No unread messages!')
    for message in messages:
        message.read = True
    db.session.commit()
    return success_response([message.serialize() for message in messages])

# Get all messages
@app.route("/api/users/<int:user_id>/messages/")
def get_all_messages(user_id):
    messages = Message.query.filter_by(receiver_id=user_id).all()
    if messages is None:
        return failure_response('No messages!')
    return success_response([message.serialize() for message in messages])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
