from datetime import datetime
from package import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)


    server_id = db.Column(db.Integer, db.ForeignKey('app_server.id'), nullable=True)
    room_id = db.Column(db.Integer, db.ForeignKey('app_server_room.id'), nullable=True)

    def __repr__(self):
        return f"""[User]
        id: {self.id},
        username: {self.username},
        email: {self.email},
        image_file: {self.image_file},
        server_id: {self.server_id},
        room_id: {self.room_id}\n\n"""


class AppServer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=150)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    rooms = db.relationship('AppServerRoom', backref='server', lazy=True)
    clients = db.relationship('User', backref='server', lazy=True)


    def __repr__(self):
        return f"""[AppServer]
        id: {self.id},
        name: {self.name},
        capacity: {self.capacity}\n\n"""


class AppServerRoom(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    # A Room belongs to a Server
    server_id = db.Column(db.Integer, db.ForeignKey('app_server.id'), nullable=False)

    clients = db.relationship('User', backref='room', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"""[AppServerRoom]
        id: {self.id},
        name: {self.name},
        clients: User IDs {[user.id for user in self.clients]}\n\n"""
