const socket = io('/show_room')
// GET TABLE ID
const url = window.location.href;
const pathname = new URL(url).pathname;
var paths = pathname.split('/')

// remove empty strings 
paths = paths.filter(e => e)

const server_id = paths[0]
const room_id = paths[1]

socket.on('connect', ()=>{
    console.log(socket.id + ' connected')

    socket.emit('join', {server_id: server_id, room_id: room_id})
    setTimeout(()=>{
        socket.emit('user_just_joined' )
    }, 120000)
})

socket.on('connected_users_count', (data)=>{
    let users_count_element = document.getElementById('active-users-count')
    users_count_element.innerHTML = 'CONNECTED USERS: ' + data.users_count
    
})


socket.on('disconnected', (user) => {
    $("#user-" + user.id + "-video-image").remove()
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


socket.on('append_video_frame', (user) => {

    var video_frame = $(`
    <div class="col-lg-4" id="user-`+ user.id +`-video-image">
    <img src="` + user.image_file + `"  height="300px" width="100%">
    </div>
    `).hide();
    $('#videos-frame-container').append(video_frame)
    video_frame.slideDown();
    
})


socket.on('append_msg', (data) => {
    let msg_container = document.getElementById('msg_container')

    let msg_div = '<div class="">'
    let msg_p = '<p><b>' + data.username + '</b>: ' + data.msg + '</p>'
    let msg_end_div = '</div>'
    
    let msg_html = msg_div + msg_p + msg_end_div
    // msg_container.innerHTML += msg_html

    $('#msg_container').prepend(msg_html)
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
        $('#msg_container').prepend(msg_html)


        socket.emit('new_msg', {room_id: room_id, msg: msg_input.value})
        msg_input.value = '';
    }
}

$(document).ready(function() {
    $('#play-game-button').click(function() {
        if($(this).text() == 'Play a Game') {
            $('#videos-frame-container').css('transform', 'scale(0.5)')

            let play_game_img = $(`
            <div class="row" id="play-game-image">
                <img src="/static/images/poker-game.png" width="100%" height="600px" alt="">
            </div>
            `).hide()
    
            $('#game-container').prepend(play_game_img)
            play_game_img.show(400)
            $(this).text('Quit')
        }
        else {
            $('#play-game-image').hide(400, () => {
                $('#play-game-image').remove()
                $(this).text('Play a Game')
                $('#videos-frame-container').css('transform', 'scale(1)');

            })

        }
    }) 
})