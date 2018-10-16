from django.shortcuts import render,reverse,redirect
from .models import Course,CourseOrder
import time,os,hmac,hashlib
from django.conf import settings
from utils import restful
from hashlib import md5
from django.views.decorators.csrf import csrf_exempt
from apps.xfzauth.decorators import xfz_login_required

# Create your views here.
def course_index(request):
    courses = Course.objects.all()
    return render(request,'course/course_index.html',context={'courses':courses})

@xfz_login_required
def course_detail(request,course_id):
    course = Course.objects.get(pk=course_id)
    # 查询课程订单如果存在，则将此信息传递给前端，用于判断是否要显示购买课程的图标
    bought = CourseOrder.objects.filter(buyer=request.user,course=course,status=2).exists()
    # print(bought)
    return render(request,'course/course_detail.html',context={
        "course":course,
        'bought':bought
    })

def course_token(request):
    # 这个video是视频文件的完整链接
    video_url = request.GET.get('video_url')
    course_id = request.GET.get('course_id')
    bought = CourseOrder.objects.filter(course_id=course_id,buyer=request.user,status=2).exists()
    if not bought:
        return restful.params_error(message='请先购买课程')
    # 设置过期时间为两个小时
    expiration_time = int(time.time()) + 2 * 60 * 60
    # USER_ID要先在settings中配置
    USER_ID = settings.BAIDU_CLOUD_USER_ID
    USER_KEY = settings.BAIDU_CLOUD_USER_KEY

    # file=http://hemvpc6ui1kef2g0dd2.exp.bcevod.com/mda-igjsr8g7z7zqwnav/mda-igjsr8g7z7zqwnav.m3u8
    # 而我们想获取的是后面的那不含扩展名的部分，下面两句就是来获取这个扩展名的
    extension = os.path.splitext(video_url)[1]  #分离得到扩展名
    media_id = video_url.split('/')[-1].replace(extension, '')

    # unicode->bytes=unicode.encode('utf-8')bytes
    key = USER_KEY.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, USER_ID, expiration_time)
    return restful.result(data={'token': token})

def course_order(request):
    course_id = request.GET.get('course_id')
    course = Course.objects.get(pk=course_id)
    bought = CourseOrder.objects.filter(buyer=request.user,course=course,status=2).exists()
    if bought:
        return redirect(reverse('course:detail'))

    order = CourseOrder.objects.create(amount=course.price, course=course, buyer=request.user, status=1)
    context = {
        'course':course,
        # 获得完整的notify_url,域名+路径获取路径
        'notify_url':request.build_absolute_uri(reverse('course:notify_url')),
        'return_url':request.build_absolute_uri(reverse('course:detail',kwargs={"course_id":course.pk})),
        'order':order
    }
    # print(context['notify_url'])
    # print(context['return_url'])
    return render(request,'course/create_order.html',context=context)

def order_key(request):
    goodsname = request.POST.get("goodsname")
    istype = request.POST.get("istype")
    notify_url =request.POST.get("notify_url")
    orderid = request.POST.get("orderid")
    price = request.POST.get('price')
    return_url = request.POST.get("return_url")

    token = 'c170cf064a14842e227406cdcfbb60ae'
    uid = 'd682c1dded27e908dd78c068'
    orderuid = str(request.user.pk)

    key = md5("".join([goodsname, istype, notify_url, orderid, orderuid, price, return_url, token, uid]).encode(
        "utf-8")).hexdigest()
    # print(key)
    return restful.result(data={'key': key})

# 用于接收paysAPI的发出的用户支付成功的请求，并会传递一些参数
@csrf_exempt
def notify_view(request):
    print('支付成功了')
    orderid = request.POST.get('orderid')
    CourseOrder.objects.filter(pk=orderid).update(status=2)
    return restful.ok()
