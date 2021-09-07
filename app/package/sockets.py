from package import sio
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from package.models import AppServerRoom, db


SHOW_SERVER_ROOM_USERS = []





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


    emit('connected_users_count', {'users_count': len(SHOW_SERVER_ROOM_USERS)}, to='show_server_room', broadcast=True)



@sio.on('new_msg', namespace='/show_server')
def _(data):
    print(current_user.username + ' sent a message on show_server_room')
    emit('append_msg', {'username': current_user.username, 'msg': data['msg']}, to='show_server_room', include_self=False)












# TABLE ROOM
# TABLE ROOM = Table{room.id}

@sio.on('connect', namespace='/show_room')
def _():
    print(f'{current_user.username} connected')



@sio.on('disconnect', namespace='/show_room')
def _():

    # SET CURRENT USER ROOM TO NONE
    room = AppServerRoom.query.get(current_user.room_id)

    print(current_user.username + ' left the Table'+ str(room.id))

    current_user.room_id = None
    db.session.commit()

    print(current_user)
    leave_room(f'Table{room.id}')


    emit('connected_users_count', {'users_count': len(room.clients)}, to=f'Table{room.id}', broadcast=True)
    emit('disconnected', {'username': current_user.username}, include_self=True, to=f'Table{room.id}', broadcast=True)

    # update table users count
    emit('update_table_users_count', {'room_id': room.id, 'table_users_count': len(room.clients)}, namespace='/show_server', to='show_server_room', broadcast=True)




@sio.on('join', namespace='/show_room')
def _(data):

    server_id = data['server_id']
    room_id = data['room_id']
    room = AppServerRoom.query.get(room_id)
    join_room(f'Table{room.id}')


    # SET CURRENT USER ROOM TO ROOM ID
    if current_user not in room.clients:
        current_user.room_id = room.id
        db.session.commit()
        print(f"{current_user.username} joined Table id: {room_id}")
        print(current_user)
    
    emit('joined', {'username': current_user.username}, to=f'Table{room.id}', broadcast=True, include_self=False)
    emit('connected_users_count', {'users_count': len(room.clients)}, to=f'Table{room.id}', broadcast=True)

    # update table users count
    emit('update_table_users_count', {'room_id': room.id, 'table_users_count': len(room.clients)}, namespace='/show_server', to='show_server_room', broadcast=True)



@sio.on('new_msg', namespace='/show_room')
def _(data):
    room_id = data['room_id']
    msg = data['msg']
    print(current_user.username + ' sent a message on Table' + room_id)
    emit('append_msg', {'username': current_user.username, 'msg': msg}, to=f'Table{room_id}', include_self=False)