// 上传至自己的服务器版本
$(function () {
    // 拿到 uploadBtn按钮
   var uploadBtn = $("#upload-btn");
   // 此处不监听点击事件（点击后要选择文件,按钮就绑定选了的图片，不需要我们做多余动作）
   // 而是监听change事件（实在选择文件后点击打开时的这个动作）
   // change事件会返回event
    uploadBtn.change(function (event) {
       // 获取按钮上的文件,this指代当前按钮，当前按钮有file这个属性
        var file = this.files[0];
        // 创建formDate表单存取文件
        var formData = new FormData();
        //这里的upfile 必须和视图函数中的file = request.FILES.get('upfile')的upfile一样
        // 也就是视图函数通过ajaxpost提交的form表单中的upfile这个属性，或者称为键来取到文件
        formData.append('upfile',file);
        xfzajax.post({
            'url':'/cms/upload_file/',
            'data':formData,
            //设置为false表示这个数据不需要处理，默认是会进行相关处理
            'processData':false,
            // 默认会将内容转换成json格式，这里是图片不需要处理
            'contentType':false,
            'success':function (result) {
                //result为ajax 的post逼叨叨那提交验证返回的结果
                if (result['code'] === 200){
                    // 将result打印到前端控制台
                    console.log(result);
                    var url = result['data']['url'];
                    // 获取缩略图输入框，将输入框的值更新为url,url从result的data中获取
                    var thumbnailInput = $("input[name='thumbnail']");
                    thumbnailInput.val(url);
                }
            }
        });

   });
});

// 上传至七牛云版本
// $(function () {
//
//     // progressGroup ：用来控制整个进度条是否需要显示
//     var progressGroup = $("#progress-group");
//     // progressbar 用来控制整个进度条的宽度
//     var progressBar = $('.progress-bar');
//     function progress(response) {
//         var percent = response.total.percent;
//         // tofixed限制小数点后面位数
//         var percentText = percent.toFixed(0) + '%';
//         console.log(percent);
//         progressBar.css({"width": percentText});
//         progressBar.text(percentText);
//     }
//
//         function error(err) {
//             console.log(err);
//             window.messageBox.showError(err.message);
//
//             progressGroup.hide();
//
//         }
//         function complete(response) {
//             // response 包含hash值和key
//             // console.log(response)
//             // 获取域名，并传入到 缩略图输入框
//             var key = response.key;
//             var domain = 'http://7xqenu.com1.z0.glb.clouddn.com/';
//             var url = domain + key;
//             var thumbnailInput = $("input[name='thumbnail']");
//             thumbnailInput.val(url);
//
//             progressGroup.hide();
//             progressBar.css({"width":'0'});
//             progressBar.text('0%');
//
//         }
//         var uploadBtn = $("#upload-btn");
//         uploadBtn.change(function () {
//             var file = this.files[0];
//             xfzajax.get({
//                 'url':'/cms/qntoken/',
//                 'success':function (result) {
//                     if (result['code'] === 200){
//                         var token = result['data']['token'];
//                         // console.log(token);
//                         var key = file.name;
//                         var putExtra = {
//                             fname: key,
//                             params: {},
//                             mimeType: null
//                         };
//                         var config = {
//                             useCdnDomain: true,
//                             region: qiniu.region.z0
//                         };
//                         var fileLoad = qiniu.upload(file,key,token,putExtra,config);
//                         fileLoad.subscribe({
//                             'next':progress,
//                             'error':error,
//                             'complete':complete
//                         });
//                         progressGroup.show();
//                     }
//                 }
//             });
//         });
//     });


// 引用ueditor
$(function () {
    // 因为ue在很多地方用到故需绑定到window上
    window.ue = UE.getEditor('editor',{
        "initialFrameHeight":400,
        'serverUrl': '/ueditor/upload/'
    });
});

// 点击发布功能
$(function () {
   var submitBtn = $('#submit-btn');
   submitBtn.click(function (event) {
       event.preventDefault();
       var btn = $(this);
       var title = $("input[name='title']").val();
       var desc = $("input[name='desc']").val();
       var category = $("select[name='category']").val();
       var thumbnail = $("input[name='thumbnail']").val();
       // 富文本框的输入内容需要调用ueditor的api接口提取
       var content = window.ue.getContent();
       // console.log(category);
       // console.log('文本以获取');
       var news_id = btn.attr('data-news-id');
       var url = '';
       if(news_id){
           url = '/cms/edit_news/';
       }else{
           url = '/cms/write_news/';
       }
       xfzajax.post({
           'url':url,
           'data':{
               'title':title,
               'desc':desc,
               'category':category,
               'thumbnail':thumbnail,
               'content':content,
               'pk':news_id
           },
           'success':function (result) {
               if(result['code'] === 200){
                   console.log(result);
                   xfzalert.alertSuccess('已成功发布',function () {
                       window.location.reload()
                   })
               }
           }
       });
   });
});