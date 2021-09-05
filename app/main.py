from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

# Configs
app.config['SECRET_KEY'] = 'Super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('app_server_room.id'), nullable=True)

    def __repr__(self):
        return f"""[User]
        id: {self.id},
        username: {self.username},
        email: {self.email},
        image_file: {self.image_file},
        room_id: {self.room_id}\n\n"""


class AppServer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=150)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    rooms = db.relationship('AppServerRoom', backref='server', lazy=True)

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


@app.route('/')
def index():
    servers = AppServer.query.all()
    return render_template('index.html', servers=servers)

@app.route('/<int:server_id>')
def show_server(server_id):
    server = AppServer.query.get(server_id)
    return render_template('show_server.html', server=server)

@app.route('/<int:server_id>/<int:room_id>')
def show_room(server_id, room_id):
    room = AppServerRoom.query.get(room_id)
    return render_template('show_room.html', room=room)



if __name__ == '__main__':
    app.run(debug=True)