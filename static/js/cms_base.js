$(function () {
   var url = window.location.href;
   var protocol = window.location.protocol;
   var host = window.location.host;
   var domain = protocol + '//' + host;
   var path = url.replace(domain,'');
   var menuList = $(".sidebar-menu li");
   for (var index=0;index<menuList.length;index++){
       var li = $(menuList[index]);
       var a = li.children("a");
       var href = a.attr("href");
       if(href === path){
           li.addClass('active');
       }
   }
});