//点击评论
$(function () {
    var submitBtn = $('#submit-comment-btn');
    var textArea = $(".comment-textarea");
    submitBtn.click(function () {
        var content = textArea.val();
        var news_id = submitBtn.attr('data-news-id');
        xfzajax.post({
            'url':'/news/add_comment/',
            'data':{
                'content':content,
                'news_id':news_id
            },
            'success':function (result) {
                if(result['code'] === 200 ){
                    // console.log(result);
                    var comment = result['data'];
                    var tp1 = template('comment-item',{"comment":comment});
                    var commentGroup = $('.comment-list-group');
                    commentGroup.prepend(tp1);
                    textArea.val('');
                }else {
                   window.messageBox.showError(result['message']);
                }
            }
        })
    })
});