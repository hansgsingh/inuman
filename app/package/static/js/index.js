const socket = io('/index')

socket.on('update_server_user_count', (data) => {
    $('#server-'+ data.server_id + '-user-count').html('USERS INSIDE: ' + data.server_users_count);
})