// arttemplate的自定义模板标签timeSince
$(function () {
    // 有template才执行下面的
    if (window.template){
        template.defaults.imports.timeSince = function (dateValue) {
        var date = new Date(dateValue);
        var datets = date.getTime();
        var nowts = (new Date()).getTime();
        var timeStamp = (nowts - datets)/1000;
        if(timeStamp < 60){
            return 'Just now';
        }
        else if(timeStamp >= 60&& timeStamp < 60*60){
            var minutes = parseInt(timeStamp/60);
            return minutes +  'minutes ago'
        }
        else if (timeStamp >= 60*60 && timeStamp < 60*60*24){
            var hours = parseInt(timeStamp/60/60);
            return hours + 'hours ago';
        }else if(timeStamp >= 60*60*24 && timeStamp < 60*60*24*30){
            var days = parseInt(timeStamp/60/60/24);
            return days + 'days ago';
        }else {
            var year = date.getFullYear();
            var month = date.getMonth();
            var minute = date.getMinutes();
            var day = date.getDay();
            var hour = date.getHours();
            return year + '/' + month + '/' + day +'/'+ hour + '/'+ minute
        }
    }
    }
});

$(function () {
   // 获取浏览器上的url
   var url = window.location.href;
   // 获取采用的是什么协议
   var protocol = window.location.protocol;
   // 获取ip和端口
   var host = window.location.host;
   // 合成域名
   var domain = protocol + '//' + host;
   var path = url.replace(domain,'');
   var menuList = $(".menu li");
   for (var index=0;index<menuList.length;index++){
       var li = $(menuList[index]);
       var a = li.children("a");
       var href = a.attr("href");
       if(href === path){
           li.addClass('active');
       }
   }
});