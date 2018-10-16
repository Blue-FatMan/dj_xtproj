from django import forms
from django.core import validators
from  django.shortcuts import reverse,redirect
from django.contrib import messages
from .models import User
from apps.forms import FormMixin

class LoginForm(forms.Form,FormMixin):
    # validator为自定义validators=[validators.RegexValidator(r'1[3~9][0~9]\d{9}',message='手机号格式错误')]
    telephone = forms.CharField(max_length=11,min_length=11,error_messages={
        "required":'必须输入手机号码',"min_length":"手机号码不能少于11位",
        "max_length":"手机号码不能超过11位"
    })
    password = forms.CharField(min_length=8,max_length=20,error_messages={
        "required":'必须输入密码',"min_length":"密码不能少于8位",
        "max_length":"密码不能超过20位"
    })
    remember = forms.BooleanField(required=False)

class RegisterForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11, min_length=11, error_messages={
        "required": '必须输入手机号码', "min_length": "手机号码不能少于11位",
        "max_length": "手机号码不能超过11位"
    })
    username = forms.CharField(max_length=30,error_messages={
        'required':"请输入用户名","max_length":"用户名长度超出范围"})
    img_captcha = forms.CharField(max_length=4,min_length=4,error_messages={
        "required": '请输入图形验证码', "min_length": "请输入四位图形验证码",
        "max_length": "请输入四位图形验证码"})
    password1 = forms.CharField(min_length=8, max_length=20, error_messages={
        "required": '必须输入密码', "min_length": "密码不能少于8位",
        "max_length": "密码不能超过20位"
    })
    password2 = forms.CharField(min_length=8, max_length=20, error_messages={
        "required": '必须输入密码', "min_length": "密码不能少于8位",
        "max_length": "密码不能超过20位"
    })
    sms_captcha = forms.CharField(max_length=4,min_length=4,error_messages={
        "required": '请输入短信验证码', "min_length": "请输入四位短信验证码",
        "max_length": "请输入短信四位验证码"})

    # 要验证某个字段是否相等，就需要重写clean方法,在验证时调用is_valid方法时会自动调用clean方法
    # def clean(self):
    def validate_data(self,request):
        cleaned_data = self.cleaned_data
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            #以下只适合传统表单
            # messages.info(request,'两次密码不一致')
            # return redirect(reverse('xfzauth:register'))
            return self.add_error('password1','两次密码不一致')

        img_captcha = cleaned_data.get('img_captcha')
        server_img_captcha = request.session.get('img_captcha')
        if img_captcha.upper() != server_img_captcha.upper():
            # messages.info(request,"图像验证码不一致请重新输入")
            # return redirect(reverse('xfzauth:register'))
            return self.add_error('img_captcha','图形验证码错误！')

        sms_captcha = cleaned_data.get('sms_captcha')
        server_sms_captcha = request.session.get('sms_captcha')
        if sms_captcha.lower() != server_sms_captcha.lower():
            # messages.info(request,"短信验证码不一致，请重新输入")
            # return redirect(reverse('xfzauth:register'))
            return self.add_error('sms_captcha','短信验证失败')

        # 如果用户存在 ，则跳转至登陆页面
        telephone = cleaned_data.get('telephone')
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            # messages.info('request','该手机号码已存在！')
            # return redirect(reverse('xfzauth:login'))
            return self.add_error('telephone','该手机号码已存在')
        return True
