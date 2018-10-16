from django.db import models

# Create your models here.
class NewsCategory(models.Model):
    name = models.CharField(max_length=100)

# aware time 清醒的时间 (知道自己所在的时区)
# navie time 幼稚的时间 (不知道自己所在的时区)
class News(models.Model):
    title = models.CharField(max_length=200)
    desc = models.CharField(max_length=300)
    thumbnail = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    # 以下是设置文章外键关联分类，当分类被删除时，分类属性设置为空，同时允许分类为空
    category = models.ForeignKey("NewsCategory",on_delete=models.SET_NULL,null=True)
    author = models.ForeignKey("xfzauth.User",on_delete=models.SET_NULL,null=True)

    class Meta:
        # 以后如果News.object 提取数据的时候，就会自动按照列表中指定的字段排序，如果不加负号，那么就是按照从小到大
        # 正序排序，加上负号就是从大到小排序
        ordering = ['-pub_time']

class Comment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    # "News",on_delete=models.CASCADE表示新闻删除了评论也会被删除
    #  related_name 用来定义别名便于反向查询时调用
    news = models.ForeignKey("News",on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey('xfzauth.User',on_delete=models.CASCADE)
    # 评论 倒叙排序
    class Meta:
        ordering = ["-pub_time"]

class Banners(models.Model):
    image_url = models.URLField()
    priority = models.IntegerField(default=0)
    link_to = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-priority']