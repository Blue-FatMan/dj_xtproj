from django.shortcuts import render
from .models import News,NewsCategory,Comment,Banners
from django.views.decorators.http import require_GET,require_POST
from django.conf import settings
from utils import restful
from .serializers import NewsSerializer
from django.http import Http404
from .forms import AddCommentForm
from .serializers import CommentSerizlizer
#  这个login_required只能针对传统的页面跳转（如果没有登陆就会跳转到login_url指定的页面）
# 但是他不能处理ajax请求，如果通过ajax请求去访问一个需求页面那么这个装饰器的页面跳转功能就不行了
# from django.contrib.auth.decorators import login_required
from apps.xfzauth.decorators import xfz_login_required
from django.db.models import Q

# Create your views here.

def index(request):
    # news = News.objects.all()
    # 查找news以及和news相关的表，如果使用all，那么模板中查询category时(即关联表的数据时)还会再查询一次数据库关联的表，
    # 这是一种优化
    newses = News.objects.select_related('author','category')[0:settings.ONE_PAGE_NEWS_COUNT]
    category = NewsCategory.objects.all()
    banners = Banners.objects.all()
    return render(request,'news/index.html',context={
        "news_list":newses,
        "category":category,
        "banners":banners,
    })

@require_GET
def news_list(request):
    """
    获取新闻列表，
    并将新闻列表返回json格式
    :param request:
    :return:
    """
    #  news/list/?p=3
    # 这里的1 为默认参数
    page = int(request.GET.get('p',1))
    category_id = int(request.GET.get('category_id',0))
    start = settings.ONE_PAGE_NEWS_COUNT*(page-1)
    end = start + settings.ONE_PAGE_NEWS_COUNT
    #  news: queryset -> [News():news()]
    # news_list = list(News.objects.all()[start:end].values())
#      values 可以将queryset转换为一个字典
#     print(category_id)
    if category_id == 0:
        # 如果category_id = 0 说明没有传category_id 过来
        newses = News.objects.all()[start:end]
    else:
        newses = News.objects.filter(category_id=category_id)[start:end]
    # 用序列化引转化成需要的json格式
    serizlizer = NewsSerializer(newses,many=True)
    return restful.result(data=serizlizer.data)


# 如果在url中定义了参数那么就必须在视图函数中定义对应的参数
def news_detail(request,news_id):
    try:
        news = News.objects.select_related('category','author').get(pk=news_id)
        context = {
            'news':news
        }
        return render(request,'news/news_detail.html',context=context)
    except News.DoesNotExist:
        # django如果raise Http404 就会自动到template 文件夹下寻找404.html文件
        raise Http404


@require_POST
@xfz_login_required
# 这个装饰器的作用是限制必须登陆才能进行评论
def add_comment(request):
    form = AddCommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        # result时json,而comment是对象，故需要将comment转化成json格式故需要将其序列化成json格式，在序列化文件中进行
        # 凡是通过create和get获取到的都不是queryset对象故不需要传递many参数
        serizlize = CommentSerizlizer(comment)
        return restful.result(data=serizlize.data)
    else:
        return restful.params_error(message=form.get_error())

def search_view(request):

    q = request.GET.get('q')
    if q:
        news_lists = News.objects.filter(Q(title__icontains=q)|Q(content__icontains=q))
        context = {
            'news_list':news_lists
        }
    else:
        news_lists = News.objects.filter().order_by('-pub_time')[0:3]
        context = {'news_list':news_lists}
    return render(request,'news/search.html',context=context)
