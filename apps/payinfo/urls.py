from django.urls import path
from  . import views

app_name = 'payinfo'

urlpatterns =[
    path('',views.payinfo_index,name='payinfo'),
    path('payinfo_order/',views.payinfo_order,name='payinfo_order'),
    path('notify_url/',views.notify_url,name='notify_url'),
    path('order_key/',views.order_key,name='order_key'),
    path('download_payinfo/',views.download_payinfo,name='download_payinfo'),
]