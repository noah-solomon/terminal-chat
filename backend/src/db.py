from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')

    def serialize(self):
        return {
        'id': self.id,
        'name': self.name,
        }

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    read = db.Column(db.Boolean, nullable=False, default=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, **kwargs):
        self.content = kwargs.get('content')
        self.date = kwargs.get('date')
        self.read = kwargs.get('read')
        self.sender_id = kwargs.get('sender_id')

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'date': self.date,
            'read': self.read,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
        }
