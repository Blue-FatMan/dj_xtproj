from django.db import models
# Create your models here.

class Payinfo(models.Model):
    price = models.FloatField()
    title = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    profile = models.CharField(max_length=300)

class PayinfoOrder(models.Model):
    # DO_NOTHING在django中不会做任何处理，完全看数据库的关系
    payinfo = models.ForeignKey('Payinfo',on_delete=models.DO_NOTHING)
    amount = models.IntegerField()
    buyer = models.ForeignKey('xfzauth.User',on_delete=models.DO_NOTHING)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 1代表支付宝 2代表微信
    is_type = models.SmallIntegerField(default=0)
    # 1 代表未支付 2代表支付完成
    status = models.SmallIntegerField(default=1)
