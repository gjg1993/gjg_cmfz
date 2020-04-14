import json
import os
import time
from django.db import transaction
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from article.models import Article,Pic
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def get_article(request):
    rows = request.GET.get('rows')
    page = request.GET.get('page', 1)
    articles = Article.objects.all().order_by('id')
    all_page = Paginator(articles, rows)
    try:
        page_obj = all_page.page(page).object_list
    except EmptyPage:
        page_obj = all_page.page(int(page) - 1).object_list
    page_data = {
        'page': page,
        'total': all_page.num_pages,
        'records': all_page.count,
        'rows': list(page_obj)
    }

    def my_default(u):
        if isinstance(u, Article):
            return {
                'id': u.id,
                'title': u.title,
                'author': u.author,
                'publish_date': u.publish_date.strftime('%Y-%m-%d'),
                'create_date': u.create_date.strftime('%Y-%m-%d'),
                'category': u.category,
                'content': u.content
            }

    data = json.dumps(page_data, default=my_default)
    return HttpResponse(data)


# 富文本上传图片所使用的的方法
@xframe_options_sameorigin  # 允许页面嵌套时发起访问
@csrf_exempt
def upload_img(request):
    file = request.FILES.get('imgFile')
    if file:
        # 获取图片所在的服务的全路径
        img_url = request.scheme + "://" +request.get_host() + "/static/pic/" + str(file)
        result = {"error": 0, "url": img_url}
        Pic.objects.create(img=file)
    else:
        result = {"error": 1, "url": "上传失败"}
    return HttpResponse(json.dumps(result), content_type="application/json")


# 找到图片所在的目录  方便进行回显
def get_all_img(request):
    pic_dir = request.scheme + "://" + request.get_host() + '/static/'
    pic_list = Pic.objects.all()
    rows = []
    for i in list(pic_list):
        # 获取图片的后缀
        path, pic_suffix = os.path.splitext(i.img.url)
        rows.append({
            "is_dir": False,
            "has_file": False,
            "filesize": i.img.size,
            "dir_path": "",
            "is_photo": True,
            "filetype": pic_suffix,
            "filename": i.img.name,
            "datetime": time.strftime('%Y-%m-%d %H:%M:%S')
        })

    data = {
        "moveup_dir_path": "",
        "current_dir_path": "",
        "current_url": pic_dir,
        "total_count": len(pic_list),
        "file_list": rows
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


def add_article(request):
    try:
        title = request.GET.get('title')
        author = request.GET.get('author')
        publish_date = request.GET.get('publish_date')
        category = request.GET.get('category')
        content = request.GET.get('content')
        with transaction.atomic():
            result = Article.objects.create(title=title, author=author, publish_date=publish_date, category=category, content=content )
            return HttpResponse(1)
    except:
        return HttpResponse(0)


def edit(request):
    try:
        article_id = request.GET.get('article_id')
        article = Article.objects.filter(id=article_id)[0]
        with transaction.atomic():
            article.title = request.GET.get('title1')
            article.author = request.GET.get('author1')
            article.publish_date = request.GET.get('publish_date1')
            article.category = request.GET.get('category1')
            article.content = request.GET.get('content1')
            article.save()
            return HttpResponse(1)
    except:
        return HttpResponse(0)


@csrf_exempt
def operate(request):
    try:
        option = request.POST.get('oper')
        if option == 'del':
            article_id = request.POST.get('id')
            with transaction.atomic():
                Article.objects.get(pk=article_id).delete()
        return HttpResponse('del')

    except:
        return HttpResponse(0)
