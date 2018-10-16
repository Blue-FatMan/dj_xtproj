$(function () {
    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' +(todayDate.getMonth() + 1) +
        '/' + todayDate.getDate();
    var options = {
        'autoclose': true,
        'showButtonPanel':true,
        'format':'yyyy/mm/dd',
        'startDate':'2017/6/1',
        'endDate':todayStr,
        'language':'zh-CN',
        'todayBtn':'linked',
        'todayHighlight':true,
        'clearBtn':true
    };
//    初始化开始日期
    $("input[name='start']").datepicker(options);
//    初始化截至时间
    $("input[name='end']").datepicker(options);

});


// 新闻列表中删除操作
$(function () {
    var deleteBtn =$('.delete-btn');
    deleteBtn.click(function () {
        var pk =$(this).attr('data-news-id');
        xfzalert.alertConfirm({
            'text':'确定要删除？',
            'confirmCallback':function () {
                xfzajax.post({
                    'url':'/cms/delete_news/',
                    'data':{
                        'pk':pk
                    },
                    'success':function (result) {
                        if(result['code'] === 200 ){
                            // window.location.reload();
                            window.location = window.location.href;
                            }
                    }
                })
            }
        })
    })
});