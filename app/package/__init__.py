from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

app = Flask(__name__)

# Configs
app.config['SECRET_KEY'] = 'Super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = '/login'
sio = SocketIO(app, ping_timeout=10)

from package import routes
from package import sockets