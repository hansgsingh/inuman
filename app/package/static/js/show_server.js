const socket = io('/show_server')

const url = window.location.href;
const pathname = new URL(url).pathname;
var paths = pathname.split('/')

// remove empty strings 
paths = paths.filter(e => e)

const server_id = paths[0]




socket.on('connect', ()=>{
    console.log(socket.id + ' connected')


    
    socket.emit('join', {server_id: server_id})

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
    
    const msg_html = msg_div + msg_p + msg_end_div
    $('#msg_container').prepend(msg_html)

})

socket.on('update_table_users_count', (data) => {
    $('#table-'+ data.room_id + '-users-count').html('users: ' + data.table_users_count);
})




function checkKey(e){
    var enterKey = 13;
    if (e.which == enterKey){
        let msg_input = document.getElementById('msg')

        let msg_div = '<div class="d-flex flex-row-reverse">'
        let msg_p = '<p><b>You<b>: ' + msg_input.value + '</p>'
        let msg_end_div = '</div>'
        
        let msg_html = msg_div + msg_p + msg_end_div
        $('#msg_container').prepend(msg_html)

        socket.emit('new_msg', {msg: msg_input.value, server_id: server_id})
        msg_input.value = '';
    }
}


// HIDE DJ
$(document).ready(function() {
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

    $(document).on('click', '.join-table', join_table);

    function join_table(button) {
        let link = $(this).data('link')



        // iframe  buttons
        let iframe_html = `
        <div class="text-center">
        <button class="btn btn-warning minimize-table mb-2 mt-4" style="width: auto;border-radius: 60px">-</button>
        <button class="btn btn-danger close-table mb-2 mt-4" style="width: auto;border-radius: 60px">X</button>
        <button class="btn btn-primary share-table mb-2 mt-4" style="width: auto;border-radius: 60px">SHARE TABLE LINK</button>

        </div>
        <iframe id="show-table-iframe" src="` + link + `"  width="100%" height="1500px" ></iframe>
        `

        // 
        socket.emit('join_room')

        let clicked_button = $(this)

        $(clicked_button, "span").text("Joining...")
        $(clicked_button, "span").attr("disabled", "disabled")


        $('#user-table-container').hide();
        $('#user-table-container').html(iframe_html);
        $.undim();

        // WAIT FOR IFRAME TO LOAD BEFORE SHOWING
        $('#show-table-iframe').on('load',()=>{
            $('#rooms').fadeOut(200)
            $('#live_chat').fadeOut(200)
            $('#user-table-container').html(iframe_html);
            $('#user-table-container').fadeIn(300);


            // scroll to user-table-container
            
            setTimeout(function() {
                $([document.documentElement, document.body]).animate({
                    scrollTop: $("#user-table-container").offset().top
                }, 500);

            }, 300)


            // CHECK IF CLICKED BUTTON IS A JOIN_TABLE_LINK FROM CHAT 
            var is_link = $(clicked_button).attr('is-link')
            if (typeof is_link !== 'undefined' && is_link !== false) {
                // ...
                $(clicked_button, "span").text("Join my table")
                $(clicked_button, "span").removeAttr("disabled")
            } else {
                $(clicked_button, "span").text("JOIN")
                $(clicked_button, "span").removeAttr("disabled")
            }


            $('.close-table').click(function(){

                $('#rooms').fadeIn(1200)
                $('#live_chat').fadeIn(1200)


                $('#user-table-container').children().fadeOut(600).promise().then(function() {
                    $('#user-table-container').empty();
                    $([document.documentElement, document.body]).animate({
                        scrollTop: $("#live_chat").offset().top
                    }, 300);


                })
                
            })
            $('.minimize-table').click(function(){

                if($(this).text() == '-') {
                    $('#rooms').fadeIn(1200)
                    $('#live_chat').fadeIn(1200)
                    let minimize_button = $(this)

                    $('#show-table-iframe').fadeOut(600).promise().then(function() {
                        $([document.documentElement, document.body]).animate({
                            scrollTop: $("#live_chat").offset().top
                        }, 300);
                        $(minimize_button).text('SHOW TABLE')
                        $(minimize_button).css('position', 'fixed')
                        $(minimize_button).css('top', '0%')
                        $(minimize_button).css('right', '29%')
                        
                        $('.close-table').text('LEAVE TABLE')
                        $('.close-table').css('position', 'fixed')
                        $('.close-table').css('top', '0%')
                        $('.close-table').css('right', '21%')

                        $('.share-table').css('position', 'fixed')
                        $('.share-table').css('top', '0%')
                        $('.share-table').css('right', '10.4%')


                    })
                } else {
                    $('#rooms').fadeOut(600)
                    $('#live_chat').fadeOut(600)
                    let minimize_button = $(this)
                    $(minimize_button).text('-')
                    $(minimize_button).css('position', '')
                    $(minimize_button).css('top', '')
                    $(minimize_button).css('right', '')

                    $('.close-table').text('X')
                    $('.close-table').css('position', '')
                    $('.close-table').css('top', '')
                    $('.close-table').css('right', '')

                    $('.share-table').css('position', '')
                    $('.share-table').css('top', '')
                    $('.share-table').css('right', '')

                    $('#show-table-iframe').fadeIn(1200).promise().then(function() {

                        $([document.documentElement, document.body]).animate({
                            scrollTop: $("#user-table-container").offset().top
                        }, 300);

                    })
                }
                
            })
            $('.share-table').click(function(){
                let msg_container = document.getElementById('msg_container')

                let msg_div = '<div class="d-flex flex-row-reverse">'
                let msg_p = '<p><b>You</b>: <button class="btn join-table" disabled>Join my table </button></p>'
                let msg_end_div = '</div>'
                
                const msg_html = msg_div + msg_p + msg_end_div
                $('#msg_container').prepend(msg_html)

                socket.emit('share_table_link')

            })


        })
    }




});
//END JOIN TABLE
