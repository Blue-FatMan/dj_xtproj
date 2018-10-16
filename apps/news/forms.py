from django import forms
from apps.forms import FormMixin

class AddCommentForm(forms.Form,FormMixin):
    # 在表单中charfield 和textfield唯一的区别就是在表单渲染成模板时会有区别
    # charfield 会被渲染成input标签，textfield会被渲染成textarea标签
    content = forms.CharField(max_length=300)
    news_id = forms.IntegerField()