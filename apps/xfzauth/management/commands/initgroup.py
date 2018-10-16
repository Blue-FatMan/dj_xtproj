from django.core.management.base import BaseCommand
from django.contrib.auth.models import  Group,Permission,ContentType
# contentType将模型和app关联
from apps.news.models import News,NewsCategory,Banners,Comment
from apps.payinfo.models import Payinfo,PayinfoOrder
from apps.course.models import Course,CourseCategory,Teacher,CourseOrder


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 编辑组
        # 确定需要哪些权限，获取contentType对象,然后在permission中筛选需要的权限
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banners),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Payinfo),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Teacher)
        ]
        edit_permissions = Permission.objects.filter(
            content_type__in=edit_content_types
        )
        edit_group = Group.objects.create(name='编辑')
        edit_group.permissions.set(edit_permissions)

        # 财务组
        finance_content_types = [
            ContentType.objects.get_for_model(PayinfoOrder),
            ContentType.objects.get_for_model(CourseOrder)
        ]
        finance_permissions = Permission.objects.filter(
            content_type__in=finance_content_types
        )
        finance_group = Group.objects.create(name='财务')
        finance_group.permissions.set(finance_permissions)

        # 管理员组,调用union将编辑和财务权限合二为一
        admin_permissions = edit_permissions.union(finance_permissions)
        admin_group = Group.objects.create(name='管理员')
        admin_group.permissions.set(admin_permissions)
        self.stdout.write(self.style.SUCCESS("初始化分组已经添加成功"))