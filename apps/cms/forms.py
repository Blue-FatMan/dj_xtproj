from apps.forms import FormMixin
from django import forms
from apps.news.models import News
from apps.news.models import Banners
from apps.course.models import Course

class EditNewsCategoryForm(forms.Form,FormMixin):
    pk = forms.IntegerField(error_messages={
        'require':'必须传入参数'})
    name = forms.CharField(max_length=100,min_length=1,error_messages={
        'require': '请输入分类名'
    })


# ModelForm可以指定表单是为哪个app服务的，而form不可以
class WriteNewsForm(forms.ModelForm,FormMixin):
    category = forms.IntegerField()
    class Meta:
        model = News
        fields = ('title','desc','thumbnail','content')
        error_messages = {
            'category':{
            },
            'title':{
                'required':"请输入标题",
                'max_length':'最大长度不超过200'
            }
        }
class EditNewsForm(WriteNewsForm):
    pk = forms.IntegerField()

class AddBannerForm(forms.ModelForm,FormMixin):
    class Meta:
        model = Banners
        fields = ('image_url','link_to','priority')


class EditBannerForm(forms.ModelForm,FormMixin):
    # 这里的id model中没有需要自定义，
    pk = forms.IntegerField()
    class Meta:
        model = Banners
        fields = ('image_url','link_to','priority')

class AddCourseForm(forms.ModelForm,FormMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()
    class Meta:
        model = Course
        # 除了以下字段其他都不要
        exclude = ('pub_time','category','teacher')