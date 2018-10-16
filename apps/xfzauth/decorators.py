from utils import restful
from django.shortcuts import redirect
from functools import wraps
from django.contrib.auth.models import Permission,ContentType
from django.http import Http404

def xfz_login_required(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登陆')
            else:
                return redirect('/account/login/')
    return wrapper

# 自定义装饰器，如果用户有权限就让其调用视图函数，否则报404错误
def xfz_permission_required(model):
    def decorator(viewfunc):
        @wraps(viewfunc)
        def _wrapper(request,*args,**kwargs):
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(
                content_type=content_type
            )
            codenames = [content_type.app_label+'.'+permission.codename for
                         permission in permissions]
            result = request.user.has_perms(codenames)
            # has_perms:只能采用字符串形式判断呢，字符串形式为 app_label.codename
            # result = request.user.has_perms(permissions)
            if result:
                return viewfunc(request,*args,**kwargs)
            else:
                raise Http404
        return _wrapper
    return decorator

def xfz_superuser_required(viewfunc):
    @wraps(viewfunc)
    def _wrapper(request,*args,**kwargs):
        if request.user.is_superuser:
            return viewfunc(request,*args,**kwargs)
        else:
            raise Http404
    return _wrapper
