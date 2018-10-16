from django.shortcuts import render,redirect,reverse
from .models import Payinfo,PayinfoOrder
from django.views.decorators.csrf import csrf_exempt
from utils import restful
from hashlib import md5
from django.conf import settings
from django.http import FileResponse
import os
from apps.xfzauth.decorators import xfz_login_required

# Create your views here.

def payinfo_index(request):
    payinfos = Payinfo.objects.all()
    context = {
        'payinfos':payinfos
    }
    return render(request,'payinfo/payinfo.html',context=context)

@xfz_login_required
def payinfo_order(request):
    payinfo_id = request.GET.get('payinfo_id')
    payinfo = Payinfo.objects.get(pk=payinfo_id)
    bought = PayinfoOrder.objects.filter(buyer=request.user,payinfo=payinfo,status=2).exists()
    if  bought:
        return redirect(reverse(
            'payinfo:download_payinfo')+ "?payinfo_id=%s"%payinfo.pk)

    order = PayinfoOrder.objects.create(payinfo=payinfo,amount=payinfo.price,buyer=request.user,
                                status=1)
    context = {
        'payinfo':payinfo,
        'order':order,
        'notify_url':request.build_absolute_uri(reverse('payinfo:notify_url')),
        'return_url':request.build_absolute_uri(reverse('payinfo:download_payinfo')+
                                                        "?payinfo_id=%s"%payinfo.pk)
    }
    return render(request,'payinfo/create_order.html',context=context)

def order_key(request):
    goodsname = request.POST.get("goodsname")
    istype = request.POST.get("istype")
    notify_url = request.POST.get("notify_url")
    orderid = request.POST.get("orderid")
    price = request.POST.get("price")
    return_url = request.POST.get("return_url")

    token = 'c170cf064a14842e227406cdcfbb60ae'
    orderuid = str(request.user.pk)
    uid = 'd682c1dded27e908dd78c068'
    print(goodsname,istype,notify_url,orderid,price,return_url,orderuid)
    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode("utf-8")).hexdigest()
    print(key)
    return restful.result(data={'key':key})

@csrf_exempt
def notify_url(request):
    orderid = request.POST.get('orderid')
    PayinfoOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()

def download_payinfo(request):
    # 如果用户没有购买，就不让其下载
    payinfo_id = request.GET.get('payinfo_id')
    payinfo = Payinfo.objects.get(pk=payinfo_id)
    bought = PayinfoOrder.objects.filter(payinfo=payinfo,buyer=request.user,
                                         status=2)
    print(bought)
    if not bought:
        return redirect(reverse('payinfo:payinfo'))
    path = payinfo.path
    # 作为一个附件形式下载，而不是作为一个普通的文件下载
    response = FileResponse(open(os.path.join(settings.MEDIA_ROOT,path),'rb'))
    # 下面这两步的设置是将文件已附件形式下载，如果不设置就会将文件渲染至浏览器
    response['Content-Type'] = 'image/jpeg'
    # 取目录的最后一部风，即文件名
    response['Content-Disposition'] = 'attachment;filename="%s"'%path.split('/')[-1]
    return response