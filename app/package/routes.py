from flask import render_template, request, redirect, url_for
from package import app
from flask_login import login_user, logout_user, current_user, login_required

from package.models import User, AppServer, AppServerRoom

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Incorrect password'
    return render_template('login.html')

@app.route('/')
def index():
    servers = AppServer.query.all()
    return render_template('index.html', servers=servers)

@app.route('/<int:server_id>')
@login_required
def show_server(server_id):
    server = AppServer.query.get(server_id)
    return render_template('show_server.html', server=server)

@app.route('/<int:server_id>/<int:room_id>')
def show_room(server_id, room_id):
    room = AppServerRoom.query.get(room_id)
    return render_template('show_room.html', room=room)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
