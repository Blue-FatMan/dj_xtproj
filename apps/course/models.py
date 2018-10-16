from django.db import models

# Create your models here.


class CourseCategory(models.Model):
    name = models.CharField(max_length=20)

class Teacher(models.Model):
    username = models.CharField(max_length=20)
    jobtitle = models.CharField(max_length=20)
    profile = models.TextField()
    avatar = models.URLField()

class Course(models.Model):
    title = models.CharField(max_length=100)
    video_url = models.URLField()
    cover_url = models.URLField()
    price = models.FloatField()
    duration = models.IntegerField()
    profile = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('CourseCategory',on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey('Teacher',on_delete=models.DO_NOTHING,default=None)

class CourseOrder(models.Model):
    pub_time = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    buyer = models.ForeignKey('xfzauth.User',on_delete=models.DO_NOTHING)
    course = models.ForeignKey('Course',on_delete=models.DO_NOTHING)
    # 1.待支付，2.已支付
    status = models.IntegerField()
    # 1.代表支付宝 2.代表微信 0.代表未知
    istype =models.SmallIntegerField(default=0)