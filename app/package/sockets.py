from package import sio
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room

SHOW_SERVER_ROOM_USERS = []
SHOW_ROOM_USERS = []
USERS_WHO_JUST_JOINED = []


@sio.on('user_just_joined', namespace='/show_server')
def _():
    print('60 SECONDS HAS PAST')
    USERS_WHO_JUST_JOINED.remove(current_user.username)


@sio.on('connect', namespace='/show_server')
def _():
    print(f'{current_user.username} connected')



@sio.on('disconnect', namespace='/show_server')
def _():
    print(current_user.username + ' left the show_server_room')
    leave_room('show_server_room')
    SHOW_SERVER_ROOM_USERS.remove(current_user.username)
    print(SHOW_SERVER_ROOM_USERS)
    emit('connected_users_count', {'users_count': len(SHOW_SERVER_ROOM_USERS)}, to='show_server_room', broadcast=True)



@sio.on('join', namespace='/show_server')
def _():
    if current_user.username not in SHOW_SERVER_ROOM_USERS:
        join_room('show_server_room')
        SHOW_SERVER_ROOM_USERS.append(current_user.username)

    if current_user.username not in USERS_WHO_JUST_JOINED:
        print(f"{current_user.username} joined show_server_room")
        USERS_WHO_JUST_JOINED.append(current_user.username)
        emit('joined', {'username': current_user.username}, to='show_server_room', include_self=False)

    emit('connected_users_count', {'users_count': len(SHOW_SERVER_ROOM_USERS)}, to='show_server_room', broadcast=True)



@sio.on('new_msg', namespace='/show_server')
def _(data):
    print(current_user.username + ' sent a message on show_server_room')
    emit('append_msg', {'username': current_user.username, 'msg': data['msg']}, to='show_server_room', include_self=False)









# TABLE ROOM

@sio.on('user_just_joined', namespace='/show_room')
def _():
    print('60 SECONDS HAS PAST')
    USERS_WHO_JUST_JOINED.remove(current_user.username)


@sio.on('connect', namespace='/show_room')
def _():
    print(f'{current_user.username} connected')



@sio.on('disconnect', namespace='/show_room')
def _():
    print(current_user.username + ' left the show_room')
    leave_room('show_room')
    SHOW_ROOM_USERS.remove(current_user.username)
    print(SHOW_ROOM_USERS)
    emit('connected_users_count', {'users_count': len(SHOW_ROOM_USERS)}, to='show_room', broadcast=True)
    emit('disconnected', {'username': current_user.username}, to='show_room', broadcast=True)



@sio.on('join', namespace='/show_room')
def _():
    if current_user.username not in SHOW_ROOM_USERS:
        join_room('show_room')
        SHOW_ROOM_USERS.append(current_user.username)

    print(f"{current_user.username} joined show_room")
    USERS_WHO_JUST_JOINED.append(current_user.username)
    emit('joined', {'username': current_user.username}, to='show_room', include_self=False)

    emit('connected_users_count', {'users_count': len(SHOW_ROOM_USERS)}, to='show_room', broadcast=True)



@sio.on('new_msg', namespace='/show_room')
def _(data):
    print(current_user.username + ' sent a message on show_room')
    emit('append_msg', {'username': current_user.username, 'msg': data['msg']}, to='show_room', include_self=False)