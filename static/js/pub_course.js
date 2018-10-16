//添加富文本编辑器
$(function () {
    window.ue = UE.getEditor('editor',{
        'serverUrl':'/ueditor/upload/',
    })
});

$(function () {
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        // 阻止默认行为，不阻止默认，就会走传统表单，就会将json数据展示在浏览器中
        event.preventDefault();

        var title = $('#title-input').val();
        var price= $('#price-input').val();
        var category_id = $('#category-select').val();
        var teacher_id = $('#teacher-select').val();
        var video_url = $('#video-input').val();
        var cover_url = $('#cover-input').val();
        var duration = $('#duration-input').val();
        // 简介为富文本框输入的，需要调用ueditor接口
        var profile = window.ue.getContent();

        xfzajax.post({
            'url':'/cms/pub_course/',
            'data':{
                'title':title,
                'category_id':category_id,
                'teacher_id':teacher_id,
                'video_url':video_url,
                'cover_url':cover_url,
                'price':price,
                'duration':duration,
                'profile':profile
            },
            'success':function (result) {
                if(result['code'] === 200){
                    xfzalert.alertSuccess('已成功发布',function () {
                    // window.location.reload();
                    window.location = window.location.href;
                   })
                }
            }
        })
    })
});