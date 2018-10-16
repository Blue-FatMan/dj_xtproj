//这个函数是用来给关闭按钮添加关闭事件的
function addCloseBannerEvent(bannerItem) {
    var closeBtn = bannerItem.find('.close-btn');
    var bannerId = bannerItem.attr('data-banner-id');
    // console.log(bannerId);
    closeBtn.click(function () {
        if(bannerId){
            xfzalert.alertConfirm({
                'text':'确定要删除吗？',
                'confirmCallback':function () {
                    xfzajax.post({
                        'url':'/cms/delete_banner/',
                        "data":{
                            'banner_id':bannerId
                        },
                        'success':function (result) {
                            if(result['code'] === 200){
                                bannerItem.remove();
                                window.messageBox.showSuccess('轮播图删除成功！')
                            }
                        }
                    });
                }
            });
        }else {
            bannerItem.remove();
        }
    });
}

//这个函数是用来绑定选择图片的事件的
function addImageSelectEvent(bannerItem) {
    var image = bannerItem.find('.banner-image');
    var imageSelect = bannerItem.find(".image-select");
    image.click(function () {
    // 只有input(type=file类型才能打开文件选择器
    // 所以想打开文件，可以隐藏一个input标签
        imageSelect.click();
    });
    //文件选择器 的点击打开操作是监听change
    imageSelect.change(function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append('upfile',file);
        xfzajax.post({
            'url':'/cms/upload_file/',
            'data':formData,
            'processData':false,
            'contentType':false,
            'success':function (result) {
                if(result['code'] ===200){
                    var url = result['data']['url'];
                    // console.log(url);
                    //修改image的src属性
                    image.attr('src',url);

                }
            }
        })
    })
}

//轮播图保存事件
function addSaveBannerEvent(bannerItem) {
    var saveBtn = $('.save-btn');
    var image = bannerItem.find(".banner-image");
    var priorityInput = bannerItem.find("input[name='priority']");
    var linktoInput = bannerItem.find("input[name='link-to']");
    var bannerId = bannerItem.attr("data-banner-id");
    var url = '';
    if(bannerId){
        url = '/cms/edit_banner/';
    }else {
        url = '/cms/add_banner/';
    }
    saveBtn.click(function () {
        var image_url = image.attr('src');
        var priority = priorityInput.val();
        var link_to = linktoInput.val();
        // console.log(image_url,priority,link_to);
        xfzajax.post({
            'url':url,
            'data':{
                'image_url':image_url,
                'priority':priority,
                'link_to':link_to,
                //即使是新增的轮播图，由于视图函数中并没有用到pk，故传过去也没问题
                'pk':bannerId
            },
            'success':function (result) {
                if(result['code'] === 200){
                    // console.log('ajax成功');
                    //如果不存在bannerId 则添加bannerId、
                    if(!bannerId){
                        bannerId = result['data']['banner_id'];
                        // var bannerId = result['data']['banner_id'];js中变量的作用域是以函数为单位的此处用var定义
                        //就表示if判断前该变量是未定义的，就会导致编辑时即id存在时会走到！bannerID中
                        // console.log(bannerId);
                        //将该bannerItem绑定一个bannerId
                        bannerItem.attr('data-banner-id',bannerId);
                        window.messageBox.showSuccess('轮播图添加成功');
                    }else {
                        window.messageBox.showSuccess('轮播图修改成功')
                    }
                    var prioritySpan = bannerItem.find(".priority-span");
                    prioritySpan.text('优先级'+priority);
                }
            }
        })
    })
}

// 针对重复操作定义一个函数专用于创建轮播图项
function createBannerItem(banner) {
    var tp1 =template("banner-item",{'banner':banner});
    var bannerItemGroup = $('.banner-list-group');
    var bannerItem = null;
    if(banner){
        bannerItemGroup.append(tp1);
        bannerItem = bannerItemGroup.find('.banner-item:last');
    }else {
        bannerItemGroup.prepend(tp1);
        bannerItem = bannerItemGroup.find('.banner-item:first');
    }
    addCloseBannerEvent(bannerItem);
    addImageSelectEvent(bannerItem);
    addSaveBannerEvent(bannerItem);
}

//绑定网页加载完成后执行获取轮播图列表的事件
$(function () {
    xfzajax.get({
        'url':'/cms/banner_list/',
        'success':function (result) {
            var banners = result['data']['banners'];
            // 将获取的数据传给arttemplate
            for (var i = 0;i <banners.length;i++){
                var banner = banners[i];
                createBannerItem(banner);
            }
        }
    })
});


// 点击添加轮播图事件
$(function () {
    var bannersBtn = $('#add-banner-btn');
    var bannerListGroup = $('.banner-list-group');
    bannersBtn.click(function () {
        var length = bannerListGroup.children().length;
        if(length >= 6){
            window.messageBox.showInfo('最多只能添加六张轮播图')
        }else {
            createBannerItem();
        }
    })
});
//由于js文件时网页加载完成后就已经绑定完，而这些轮播图在网页加载完还没有，
// 故删除时间此时无法绑定在删除按钮上，故不能按以下情况添加绑定删除
// $(function () {
//    var deleteBtn = $('#delete-banner-btn');
//    deleteBtn.click(function () {
//
//    });
// });

// 给

