from package import sio
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room

SHOW_SERVER_ROOM_USERS = []


@sio.on('connect', namespace='/show_server')
def _():
    print(f'{current_user.username} connected')


@sio.on('disconnect', namespace='/show_server')
def _():
    print(current_user.username + ' left the show_server_room')
    leave_room('show_server_room')
    SHOW_SERVER_ROOM_USERS.remove(current_user.username)


@sio.on('join', namespace='/show_server')
def _():
    SHOW_SERVER_ROOM_USERS.append(current_user.username)
    join_room('show_server_room')
    print(f"{current_user.username} joined show_server_room")
    emit('joined', {'username': current_user.username}, broadcast=True)


@sio.on('new_msg', namespace='/show_server')
def _(data):
    emit('append_msg', {'username': current_user.username, 'msg': data['msg']}, to='show_server_room', include_self=False)