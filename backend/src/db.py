from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# your classes here


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sent_messages = db.relationship(
        'Message', backref='sender', lazy=True, foreign_keys='Message.sender_id')
    received_messages = db.relationship(
        'Message', backref='receiver', lazy=True, foreign_keys='Message.receiver_id')

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')

    def get_all_messages(self):
        return self.received_messages

    def get_unread_messages(self):
        return [message for message in self.received_messages if not message.read]

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @staticmethod
    def get_name_from_id(id):
        query = User.query.filter_by(id=id)
        if query.first() is None:
            return "<no name>"
        return query.first().name


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    read = db.Column(db.Boolean, nullable=False, default=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    # sender = db.relationship("User", foreign_keys=[sender_id])
    # receiver = db.relationship("User", foreign_keys=[receiver_id])

    def __init__(self, **kwargs):
        self.content = kwargs.get('content')
        self.date = kwargs.get('date')
        self.read = kwargs.get('read')
        self.sender_id = kwargs.get('sender_id')
        self.receiver_id = kwargs.get('receiver_id')

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'date': str(self.date),
            'read': self.read,
            'sender_id': self.sender_id,
            # User.get_name_from_id(self.sender_id),
            'sender_name': User.get_name_from_id(self.sender_id),
            'receiver_id': self.receiver_id,
        }
