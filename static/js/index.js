

// 加载更多新闻事件
$(function () {
    var loadBtn = $('.load-more-btn');
    loadBtn.click(function () {
        var li = $(".list-tab-group li.active");
        var category_id = li.attr('data-category-id');
        var page = parseInt(loadBtn.attr('data-page'));
        console.log('分类',category_id);
        console.log('page',page);
        xfzajax.get({
            'url':'/list/',
            'data':{
                'p':page,
                'category_id':category_id
            },
            'success':function (result) {
                // console.log(result);
                var newses = result['data'];
                if (newses.length >= 1){
                    var tp1 = template("news-item",{"newses":newses});
                    var newsListGroup = $(".news-list-group");
                    console.log(newsListGroup);
                    newsListGroup.append(tp1);
                    // console.log(newsListGroup);
                    page += 1;
                    loadBtn.attr('data-page',page);
                }else {
                    window.messageBox.showInfo('没有更多数据了');
                }
            }
        })
    });
});


// 点击新闻分类切换新闻列表
$(function () {
    var categoryUl = $(".list-tab-group");
    var liTags = categoryUl.children();
    var loadBtn = $('.load-more-btn');
    liTags.click(function () {
        var li = $(this);
        var categoryID = li.attr('data-category-id');
        // console.log(categoryID);
        xfzajax.get({
            'url':'list/',
            'data':{
                'category_id':categoryID
            },
            'success':function (result) {
                // console.log(result);
                var newses = result['data'];
                // tp1 获取当前分类下的所有新闻
                var tp1 = template("news-item",{"newses":newses});
                var newsListGroup = $(".news-list-group");
                // 清空新闻列表
                newsListGroup.empty();
                // 新闻列表中添加tp1的新闻
                newsListGroup.append(tp1);
                //  移出该li标签的所有兄弟标签的active
                li.addClass('active').siblings().removeClass('active');
                loadBtn.attr('data-page',2);
            }
        });
    });
});