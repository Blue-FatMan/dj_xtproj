from django.shortcuts import render,redirect,reverse
from apps.xfzauth.models import User
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.models import Group
from apps.xfzauth.decorators import xfz_superuser_required
from django.utils.decorators import method_decorator

@xfz_superuser_required
def staffs(request):
    context = {
        'staffs':User.objects.filter(Q(is_staff=True)|Q(is_superuser=True))
    }
    return render(request,'cms/staffs.html',context=context)

@method_decorator(xfz_superuser_required,name='dispatch')
class AddStaffView(View):
    def get(self,request):
        context = {
            'groups':Group.objects.all()
        }
        return render(request,'cms/add_staffs.html',context=context)

    def post(self,request):
        telephone = request.POST.get('telephone')
        user = User.objects.get(telephone=telephone)
        # print('添加的用户',user.username,user.is_staff)
        user.is_staff = True
        # print('该用户是否是员工',user.is_staff)
        group_ids = request.POST.getlist('groups')
        groups = Group.objects.filter(pk__in=group_ids)
        # 下面这一步是将用户和分组绑定
        user.groups.set(groups)
        # 绑定操作后要保存才能生效
        user.save()
        return redirect(reverse('cms:staffs'))