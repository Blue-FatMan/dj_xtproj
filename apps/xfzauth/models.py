from django.contrib.auth.models import  AbstractBaseUser,\
    PermissionsMixin,BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self,telephone,username,password,**kwargs):
        user = self.model(telephone=telephone, username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_user(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(telephone,username,password,**kwargs)

    def create_superuser(self,telephone,username,password,**kwargs):
        kwargs['is_superuser'] = True
        return self._create_user(telephone, username, password, **kwargs)

class User(AbstractBaseUser,PermissionsMixin):
    telephone = models.CharField(max_length=11,unique=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True,null=True)
    is_active = models.BooleanField(default=True)
    gender = models.IntegerField(default=0) # 0带你未知，1代表男2代表女
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    #USERNAME_FIELD 这个属性是以后再使用authenticate进行验证的字段默认是username 这里改成telephone
    USERNAME_FIELD = 'telephone'
    #这个属性是用于create super user命令是要输入的字段，这里值需要写一个username
    #以后再创建超级管理员时，就会让输入USERNAME_FIELD指定的字段
    #现在指定的是telephone以及password（这个不指定也会要求输入)
    REQUIRED_FIELDS = ['username']
    # 以后给某个用户发送邮箱时候，会使用该属性来发送
    EMAIL_FIELD = 'email'
    # 这样以后就可使用User.objects.create_user()创建用户User.objects.create_superuser()
    objects = UserManager()


    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

