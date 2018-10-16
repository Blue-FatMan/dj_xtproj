from rest_framework import serializers
from .models import News,NewsCategory
from apps.xfzauth.serializers import UserSerializer
from .models import Comment


class NewsCategorySerizlizer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id','name')

# 将模型数据序列化成json格式,以便于视图处理时前端接收（json）
class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerizlizer()
    author = UserSerializer()
    class Meta :
        model = News
        fields = ('id','title','desc','thumbnail','pub_time','category','author')

class CommentSerizlizer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta :
        model = Comment
        fields = ('content','news','id','author','pub_time')

