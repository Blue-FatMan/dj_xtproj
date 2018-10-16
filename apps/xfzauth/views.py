from django.shortcuts import render,reverse,redirect
from  django.views.generic import View
from  .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from utils.captcha.hycaptcha import Captcha
from django.http import HttpResponse
from  io import BytesIO
from utils.aliyunsdk import aliyun
from .models import User
from utils import restful

# def login_view(request):
#     if request.method == 'GET':
#         return render(request,'login/login.html')

class LoginView(View):
    def get(self,request):
        return render(request,"login/login.html")

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get("telephone")
            password = form.cleaned_data.get("password")
            remember = form.cleaned_data.get("remember")
            user = authenticate(request,username=telephone,password=password)
            if user:
                login(request,user)
                if remember:
                    #默认过期时间位两周
                    request.session.set_expiry(None)
                else:
                    #0 表示浏览器关闭及结束
                    request.session.set_expiry(0)
                #登陆成功跳转到首页
                return redirect(reverse("news:index"))
            else:
                messages.info(request,'请输入正确的用户名或密码')
                return redirect(reverse('xfzauth:login'))
        else:
            messages.info(request,'你的用户名或密码是错的')
            return redirect(reverse("xfzauth:login"))

# form版本的注册
# class RegisterView(View):
#     def get(self,request):
#         return render(request,'login/register.html')
#     def post(self,request):
#         form = RegisterForm(request.POST)
#         if form.is_valid() & form.validate_data(request):
#             telelphone = form.cleaned_data.get('telephone')
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = User.objects.create_user(telephone=telelphone,
#                                             username=username,password=password)
#             login(request,user)
#             return redirect(reverse('news:index'))
#         else:
#             # print(type(form.errors))
#             # print(form.errors.get_json_data())
#             #{"telephone":[{"message":"手机号码个数必须为11位！"}]}
#             # get_error为另定义的方法，用于获取错误信息
#             message = form.get_error()
#             messages.info(request,message)
#             return redirect(reverse('xfzauth:register'))

# ajax版本的注册
class RegisterView(View):
    def get(self,request):
        return render(request,'login/register.html')

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid() and form.validate_data(request):
            # 先验证数据是否合法
            telephone = form.cleaned_data.get('telephone')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # print('手机号码%s'%telephone)
            user = User.objects.create_user(telephone=telephone,username=username,
                                            password=password)
            login(request,user)
            return restful.ok()
        else:
            message =form.get_error()
            return restful.params_error(message=message)
        # return  HttpResponse('success')



def image_captcha(request):
    text,image = Captcha.gene_code()
    # image 不是一个Httpresponse可识别的对象
    # 因此先要将image变成一个数据流才能放到Httpresponse上
    # bytesIO  相当于一个管道， 可以用来存储二进制字节流
    print('获取image',text,image)
    out = BytesIO()
    image.save(out,'png')
    out.seek(0) # 设置文件指针
    response = HttpResponse(content_type='image/png')
    response.write(out.read())
    response['Content-length'] = out.tell()
    request.session['img_captcha'] = text
    return response

def sms_captcha(request):
    code = Captcha.gene_text()
    # account/sms_captcha/?telephone=12345678900 获取telephone
    telephone = request.GET.get('telephone')
    request.session['sms_captcha'] = code
    # print(telephone)
    # print('短信验证码：%s '%code)
    result = aliyun.send_sms(telephone,code=code)
    return HttpResponse('success')

def logoutView(request):
    logout(request)
    return redirect(reverse('news:index'))