from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from apps.news.models import NewsCategory,News,Banners
from utils import restful
from .forms import EditNewsCategoryForm,WriteNewsForm,EditNewsForm
from django.conf import settings
import os
import qiniu
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.cms.forms import AddBannerForm,EditBannerForm
from django.core.paginator import Paginator
from datetime import datetime
from urllib import parse
from django.utils.timezone import localtime
import datetime
from  django.contrib.auth.decorators import permission_required
from apps.xfzauth.decorators import xfz_permission_required
# Create your views here.

# 这个装饰器用来验证是否有权限登陆后台，没有就会跳转至首页
@staff_member_required(login_url='/')
def cms_index(request):
    # category = NewsCategory.objects.first()
    # for x in range(0,50):
    #     title = '标题%s'%x
    #     content = '内容%s'%x
    #     thumbnail = 'http://www.baidu.com/xx.png',
    #     desc = '描述信息%s'%x
    #     News.objects.create(title=title,content=content,thumbnail=thumbnail,desc=desc,category=category,author=request.user)
    return  render(request,'cms/index.html')

# @method_decorator([permission_required('news.change_news')],
#                   name='dispatch')
# 使用自定义的装饰器
@method_decorator([xfz_permission_required(News)],name='dispatch')
class NewsList(View):
    def get(self,request):
        page = int(request.GET.get('p', 1))
        start = request.GET.get('start','2018/8/1')
        local_time = localtime().date().strftime('%Y/%m/%d')
        end = request.GET.get('end',local_time)
        title = request.GET.get('title','')
        category_id = int(request.GET.get('category',0))


        newses = News.objects.select_related('category', 'author')

        # 过滤出指定时间之内的新闻
        if start and end:
            start_date = datetime.datetime.strptime(start,'%Y/%m/%d')
            end_date = datetime.datetime.strptime(end,'%Y/%m/%d')+ datetime.timedelta(days=1)
            newses = newses.filter(pub_time__range=(start_date,end_date))

        # 过滤出标题中函数指定关键字的新闻
        if title:
            newses = newses.filter(title__icontains=title)

        if category_id != 0:
            newses = newses.filter(category=category_id)

        paginator = Paginator(newses, 2)
        page_obj = paginator.page(page)

        pagination_data = self.get_pagination_data(paginator,page_obj)

        # start=2018/7/19
        # end=2018/7/20
        # ?start=xx&end=xxx
        context = {
            'categories': NewsCategory.objects.all(),
            'paginator': paginator,
            'page_obj': page_obj,
            'newses': page_obj.object_list,
            'title': title,
            'start': start,
            'end': end,
            'category_id': category_id,
            'url_query': "&"+parse.urlencode({
                "start":start,
                "end":end,
                "title": title,
                'category': category_id
            })
        }
        # start=2018%2F07%2F01&end=2018%2F07%2F17&title=&category=0
        # print(context['url_query'])
        context.update(pagination_data)
        return render(request, 'cms/news_list.html', context=context)

    # < 1,...,30,31,32,33,34,...,52,>
    # < 1,2,3,4
    def get_pagination_data(self,paginator,page_obj,around_count=2):
        current_page = page_obj.number
        num_pages = paginator.num_pages

        # 是否左边应该出现三个点
        left_has_more = False
        # 是否右边应该出现三个点
        right_has_more = False

        # 1,...,3,4,[5]
        # [48],49,50,...,52
        if current_page <= around_count + 2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page - around_count, current_page)

        if current_page >= num_pages - around_count - 1:
            right_pages = range(current_page + 1, num_pages + 1)
        else:
            right_has_more = True
            right_pages = range(current_page + 1, current_page + around_count + 1)

        return {
            'left_pages': left_pages,
            'right_pages': right_pages,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'num_pages': num_pages
        }

@method_decorator([xfz_permission_required(News)],name='dispatch')
class EditNewsView(View):
    def get(self,request):
        pk = request.GET.get('pk')
        news = News.objects.get(pk=pk)
        categories = NewsCategory.objects.all()
        return render(request,'cms/write_news.html',context={'news':news,
                                                             'categories':categories})
    def post(self,request):
        form = EditNewsForm(request.POST)
        if form.is_valid():
            pk = form.cleaned_data.get('pk')
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            print(thumbnail)
            content = form.cleaned_data.get('content')
            category_id =form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.filter(pk=pk).update(
                title=title,desc=desc,thumbnail=thumbnail,content=content,
                category=category
            )
            return restful.ok()
        else:
            return restful.params_error(message=form.get_error())

# 删除新闻是个函数故不需要用method_decorator
@xfz_permission_required(News)
def delete_news(request):
    pk = request.POST.get('pk')
    News.objects.filter(pk=pk).delete()
    return restful.ok()

# method_decorator是将装饰器写在类视图上时使用的,name指定需要装饰的方法

@method_decorator([xfz_permission_required(News),
                   login_required(login_url='/account/login/')],
                  name='dispatch')
class WriteNewsView(View):
    def get(self,request):
        categories = NewsCategory.objects.all()
        return render(request,'cms/write_news.html',context={
            'categories':categories
        })

    def post(self,request):
        # print('进入了post视图中')
        form = WriteNewsForm(request.POST)
        # print('表单已经生成')
        if form.is_valid():
            # print('验证')
            # cleaned_data 这个属性必须在is_valid之后才会生成
            title =form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.create(title=title,desc=desc,thumbnail=thumbnail,
                                content=content,category=category,author=request.user)
            # print('文章已创建')
            return restful.ok()
        else:
            # print(request.POST)
            return restful.params_error(message=form.get_error())

    #  无论get还是post最后都要执行dispatch方法 diaspatch时View的内置方法
    # def dispatch(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         return self.post(request)
    #     if request.method == 'GET':
    #         return self.get(request)

@xfz_permission_required(NewsCategory)
def news_category(request):
    categories = NewsCategory.objects.all().order_by('-id')
    return render(request,'cms/news_category.html',context={
        "categories":categories,
    })

# 这个装饰器表示只能使用post请求调用
@require_POST
@xfz_permission_required(NewsCategory)
def add_news_category(request):
    name = request.POST.get('name')
    exists = NewsCategory.objects.filter(name=name).exists()
    if not exists:
        NewsCategory.objects.create(name=name)
        return restful.ok()
    else:
        return restful.params_error(message="该分类已经存在")

@require_POST
@xfz_permission_required(NewsCategory)
def edit_news_category(request):
    form = EditNewsCategoryForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        name = form.cleaned_data.get('name')
        try:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message='这个分类不存在！')
    else:
        return restful.params_error(message=form.get_error())

@require_POST
@xfz_permission_required(NewsCategory)
def delete_news_category(request):
    pk = request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message='这个分类不存在！')

@require_POST
@staff_member_required(login_url='/')
def upload_file(request):
    # 类似request.POST.get获取post请求的数据，request.FILES.get获取上传的文件
    file = request.FILES.get('upfile')
    if not file:
        return restful.params_error(message='没有上传任何文件')
    # 获取的文件一般放在media文件夹中,media配置和static类似
    # 因为需要读取setting中media配置 故需要从django.conf中导入settings
    name = file.name
    file_path = os.path.join(settings.MEDIA_ROOT,name)
    with open(file_path,'wb') as fp:
        for chunk in file.chunks():
            # 这个chunk是将文件分段一点一点写入，防止内存溢出
            fp.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL+name)
    return restful.result(data={'url':url})

@require_GET
@staff_member_required(login_url='/')
def qntoken(request):
    access_key = 'M4zCEW4f9XPanbMN-Lb9O0S8j893f0e1ezAohFVL'
    secret_key = '7BKV7HeEKM3NDJk8_l_C89JI3SMmeUlAIatzl9d4'

    q = qiniu.Auth(access_key,secret_key)

    bucket = 'hyvideo'

    token = q.upload_token(bucket)

    return restful.result(data={
        'token':token,
    })

@xfz_permission_required(Banners)
def banners(request):
    return render(request,'cms/banners.html')

@xfz_permission_required(Banners)
def add_banners(request):
    form = AddBannerForm(request.POST)
    if form.is_valid():
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        priority = form.cleaned_data.get('priority')
        banner = Banners.objects.create(image_url=image_url,link_to=link_to,priority=priority)
        # print('数据返回')
        return restful.result(data={'banner_id':banner.pk})
    else:
        # print(form.get_error())
        return restful.params_error(message=form.get_error())

@xfz_permission_required(Banners)
def banner_list(request):
    # values 返回的还是queryset，但其中包含的是一个字典
    #  因为这里不涉及外键，所有不需要进行序列化，
    banners = list(Banners.objects.all().values())
    return  restful.result(data={"banners":banners})

@xfz_permission_required(Banners)
def delete_banner(request):
    banner_id = request.POST.get('banner_id')
    Banners.objects.filter(pk=banner_id).delete()
    return restful.ok()

@xfz_permission_required(Banners)
def edit_banner(request):
    form = EditBannerForm(request.POST)
    if form.is_valid():
        pk = form.cleaned_data.get('pk')
        image_url = form.cleaned_data.get('image_url')
        link_to = form.cleaned_data.get('link_to')
        priority = form.cleaned_data.get('priority')
        Banners.objects.filter(pk=pk).update(image_url=image_url,
                                             link_to=link_to,priority=priority)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_error())
