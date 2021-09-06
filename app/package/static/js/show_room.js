const socket = io('/show_room')

socket.on('connect', ()=>{
    console.log(socket.id + ' connected')

    socket.emit('join')
    setTimeout(()=>{
        socket.emit('user_just_joined')
    }, 120000)
})

socket.on('connected_users_count', (data)=>{
    let users_count_element = document.getElementById('active-users-count')
    users_count_element.innerHTML = 'CONNECTED USERS: ' + data.users_count
})


socket.on('disconnected', (user) => {
    let msg_div = '<div class="d-flex justify-content-center">'
    let msg_p = '-------------- ' + user.username + '</b> left the room --------------'
    let msg_end_div = '</div>'
    
    let msg_html = msg_div + msg_p + msg_end_div
    msg_container.innerHTML += msg_html
})


socket.on('joined', (user)=>{
    console.log(user.username + ' connected')

    let msg_div = '<div class="d-flex justify-content-center">'
    let msg_p = '-------------- ' + user.username + '</b> joined the room --------------'
    let msg_end_div = '</div>'
    
    let msg_html = msg_div + msg_p + msg_end_div
    msg_container.innerHTML += msg_html
})

socket.on('append_msg', (data) => {
    let msg_container = document.getElementById('msg_container')

    let msg_div = '<div class="d-flex flex-row">'
    let msg_p = '<p><b>' + data.username + '</b>: ' + data.msg + '</p>'
    let msg_end_div = '</div>'
    
    let msg_html = msg_div + msg_p + msg_end_div
    msg_container.innerHTML += msg_html
})


function checkKey(e){
    var enterKey = 13;
    if (e.which == enterKey){
        let msg_input = document.getElementById('msg')
        let msg_container = document.getElementById('msg_container')

        let msg_div = '<div class="d-flex flex-row-reverse">'
        let msg_p = '<p><b>You<b>: ' + msg_input.value + '</p>'
        let msg_end_div = '</div>'
        
        let msg_html = msg_div + msg_p + msg_end_div
        msg_container.innerHTML += msg_html
        socket.emit('new_msg', {msg: msg_input.value})
        msg_input.value = '';
    }
}

$(document).ready(function() {
    $('#play-game-button').click(function() {
        if($('#video-image').attr('src') === '/static/images/table_room.jpg') {
            $('#video-image').attr('src', '/static/images/poker-game.png')
            $(this).text('Back')
        }
        else {
            $('#video-image').attr('src', '/static/images/table_room.jpg')
            $(this).text('Play a Game')

        }
    })
})