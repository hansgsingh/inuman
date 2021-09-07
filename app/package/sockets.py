from package import sio
from flask_login import current_user
from flask import url_for
from flask_socketio import emit, join_room, leave_room
from package.models import AppServer, AppServerRoom, db



# SERVER ROOM
# SERVER ROOM = Server{server.id}

@sio.on('connect', namespace='/show_server')
def _():
    print(f'{current_user.username} connected to /show_server')


@sio.on('join', namespace='/show_server')
def _(data):

    server = AppServer.query.get(data['server_id'])
    server_room_name = f'Server{server.id}'

    if current_user not in server.clients:
        join_room(f'Server{server.id}')
        current_user.server_id = server.id
        db.session.commit()
        print(f"{current_user.username} connected to Server{server.id}")

    emit('connected_users_count', {'users_count': len(server.clients)}, to=server_room_name, broadcast=True)
    
    emit('update_server_user_count', {'server_id': server.id, 'server_users_count': len(server.clients)}, namespace='/index', broadcast=True)


@sio.on('disconnect', namespace='/show_server')
def _():
    server = AppServer.query.get(current_user.server_id)
    server_room_name = f'Server{server.id}'
    
    
    # if current user is in table, disconnect
    if current_user.room_id != None:
        room = AppServerRoom.query.get(current_user.room_id)
        leave_room(f'Table{room.id}')
        current_user.room_id = None
        db.session.commit()
        emit('update_table_users_count', {'room_id': room.id, 'table_users_count': len(room.clients)}, namespace='/show_server', to=server_room_name, broadcast=True)

    print(current_user.username + ' left Server' + str(server.id))
    leave_room(f'Server{server.id}')

    current_user.server_id = None
    db.session.commit()


    emit('connected_users_count', {'users_count': len(server.clients)}, to=server_room_name, broadcast=True)

    emit('update_server_user_count', {'server_id': server.id, 'server_users_count': len(server.clients)}, namespace='/index', broadcast=True)



@sio.on('new_msg', namespace='/show_server')
def _(data):

    server = AppServer.query.get(data['server_id'])

    server_room_name = f'Server{server.id}'
    msg = data['msg']

    print(current_user.username + ' sent a message on Server' + str(server.id))
    emit('append_msg', {'username': current_user.username, 'msg': msg}, to=server_room_name, include_self=False)




# TABLE ROOM
# TABLE ROOM = Table{room.id}

@sio.on('connect', namespace='/show_room')
def _():
    print(f'{current_user.username} connected')



@sio.on('disconnect', namespace='/show_room')
def _():
    if current_user.server_id != None and current_user.room_id != None:
        # SET CURRENT USER ROOM TO NONE
        room = AppServerRoom.query.get(current_user.room_id)
        print(current_user.username + ' left the Table'+ str(room.id))
        server = AppServer.query.get(current_user.server_id)
        server_room_name = f'Server{server.id}'

        current_user.room_id = None
        db.session.commit()

        print(current_user)
        leave_room(f'Table{room.id}')


        emit('connected_users_count', {'users_count': len(room.clients)}, to=f'Table{room.id}', broadcast=True)
        emit('disconnected', {'id': current_user.id, 'username': current_user.username}, include_self=True, to=f'Table{room.id}', broadcast=True)

        # update table users count on /show_server nsp
        emit('update_table_users_count', {'room_id': room.id, 'table_users_count': len(room.clients)}, namespace='/show_server', to=server_room_name, broadcast=True)




@sio.on('join', namespace='/show_room')
def _(data):

    server_id = data['server_id']
    room_id = data['room_id']

    server = AppServer.query.get(server_id)
    server_room_name = f'Server{server.id}'

    room = AppServerRoom.query.get(room_id)
    join_room(f'Table{room.id}')


    # SET CURRENT USER ROOM TO ROOM ID
    if current_user not in room.clients:
        current_user.room_id = room.id
        db.session.commit()
        print(f"{current_user.username} joined Table id: {room_id}")
        print(current_user)
    
    user_img = '/static/images/' + current_user.image_file
    
    emit('joined', {'username': current_user.username}, to=f'Table{room.id}', broadcast=True, include_self=False)
    emit('connected_users_count', {'users_count': len(room.clients)}, to=f'Table{room.id}', broadcast=True)
    
    
    emit('append_video_frame', {'id': current_user.id, 'image_file': user_img}, to=f'Table{room.id}', broadcast=True, include_self=True)

    # update table users count on /show_server nsp
    emit('update_table_users_count', {'room_id': room.id, 'table_users_count': len(room.clients)}, namespace='/show_server', to=server_room_name, broadcast=True)



@sio.on('new_msg', namespace='/show_room')
def _(data):
    room_id = data['room_id']
    msg = data['msg']
    print(current_user.username + ' sent a message on Table' + room_id)
    emit('append_msg', {'username': current_user.username, 'msg': msg}, to=f'Table{room_id}', include_self=False)