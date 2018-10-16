from  django.urls import path
from  . import views

#设置命名空间,用于url反转，避免同名url冲突
app_name = 'news'

urlpatterns = [
    path('',views.index,name='index'),
    path('detail/<news_id>/',views.news_detail,name='detail'),
    path('search/',views.search_view,name='search'),
    path('list/',views.news_list,name='news_list'),
    path('add_comment/',views.add_comment,name='comment'),

]