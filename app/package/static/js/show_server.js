const socket = io('/show_server')

socket.on('connect', ()=>{
    console.log(socket.id + ' connected')

    socket.emit('join')

})

socket.on('connected_users_count', (data)=>{
    let users_count_element = document.getElementById('active-users-count')
    users_count_element.innerHTML = 'CONNECTED USERS: ' + data.users_count
})




socket.on('append_msg', (data) => {
    let msg_container = document.getElementById('msg_container')

    let msg_div = '<div class="d-flex flex-row">'
    let msg_p = '<p><b>' + data.username + '</b>: ' + data.msg + '</p>'
    let msg_end_div = '</div>'
    
    let msg_html = msg_div + msg_p + msg_end_div
    msg_container.innerHTML += msg_html
})

socket.on('update_table_users_count', (data) => {
    $('#table-'+ data.room_id + '-users-count').html('users: ' + data.table_users_count);
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
    // HIDE DJ
    $('#hide-show-dj').hide()
    $('#dj-iframe').on('load', ()=>{
        $('#hide-show-dj').show()
    })
    $('#hide-show-dj').click(function() {
        if($('#dj-iframe').is(":visible")) {
            $('#dj-iframe').hide(400)
            $('#hide-show-dj-button').html('&#8595;')

        } else {
            $('#hide-show-dj-button').html('&#8593;')
            $('#dj-iframe').show(400)
            

        }
    })



    $(".round").on({
        mouseenter: function () {
            //stuff to do on mouse enter
            $(this).css('transform', 'scale(1.5)');
            $(this).dimBackground();
        },
        mouseleave: function () {
            $(this).css('transform', 'scale(1.0)');
            $.undim();

        }
    });


})







// JOIN TABLE
$(document).ready(function() {
    $('#user-table-container').empty();

    $('.join-table').click(function(){
        let link = $(this).data('link')
        // iframe  buttons

        let iframe_html = `
        <div class="text-center">
        <button class="btn btn-warning minimize-table mb-2" style="width: 38px;border-radius: 60px">-</button>
        <button class="btn btn-danger close-table mb-2" style="width: 38px;border-radius: 60px">X</button>

        </div>
        <iframe id="show-table-iframe" src="` + link + `" width="100%" height="1000"></iframe>
        `

        // 
        socket.emit('join_room', )

        let clicked_button = $(this)

        $(clicked_button, "span").text("Joining...")
        $(clicked_button, "span").attr("disabled", "disabled")


        $('#user-table-container').hide();
        $('#user-table-container').html(iframe_html);
        $.undim();

        // WAIT FOR IFRAME TO LOAD BEFORE SHOWING
        $('#show-table-iframe').on('load',()=>{
            $('#rooms').hide(300)
            $('#user-table-container').html(iframe_html);
            $('#user-table-container').show();


            // scroll to user-table-container
            
            setTimeout(function() {
                $([document.documentElement, document.body]).animate({
                    scrollTop: $("#user-table-container").offset().top
                }, 500);
            }, 300)

            $(clicked_button, "span").text("JOIN")
            $(clicked_button, "span").removeAttr("disabled")

            $('.close-table').click(function(){
                $('#user-table-container').children().fadeOut(400).promise().then(function() {
                    $('#user-table-container').empty();
                    $('#rooms').show(400)
                    $([document.documentElement, document.body]).animate({
                        scrollTop: $("#rooms").offset().top
                    }, 500);
                });
                
            })

        })
    })


});
//END JOIN TABLE
