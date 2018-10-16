$(function () {
    var span = $('.video-container span');
    var video_url = span.attr('data-video-url');
    var cover_url = span.attr('data-cover-url');
    var course_id = span.attr('data-course-id');
    var player = cyberplayer('playercontainer').setup({
        width:'100%',
        height:'100%',
        file:video_url,
        image:cover_url,
        autostart:false,
        stretching:'uniform',
        repeat:false,
        volume:100,
        controls:true,
        // primary:'flash',
        tokenEncrypt:'true',
        // AccessKey
        ak:'3a53fc515371452fb47626ae8cdc9e1c'
    });
    // 获取token
    player.on("beforePlay",function (e) {
        // 判断是否经过加密的即判断是否是m3u8格式，没加密就不需要获取token
        if(!/m3u8/.test(e.file)){
            return;
        }
        xfzajax.get({
            'url':'/course/course_token/',
            'data':{
                'video_url':video_url,
                'course_id':course_id
            },
            'success':function (result) {
                if(result['code'] === 200){
                    var token = result['data']['token'];
                    player.setToken(e.file,token);
                }else {

                    window.messageBox.showError(result['message']);
                    player.stop();
                }
            }
        })

    })
});