import hashlib
import json
import random,time
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from admins.models import TChapter,TUser,TGhosa,TImage,UserInfo
from article.models import Article
# Create your views here.


def first_page(request):
    user_id = request.GET.get("uid")
    type = request.GET.get("type")
    sub_type = request.GET.get("sub_type")
    user_id = UserInfo.objects.filter(pk=user_id).first()
    if not user_id:
        data = {
            'status': 401,
            'msg': "用户未登陆"
        }
        return HttpResponse(json.dumps(data))

    # 代表访问的事首页
    if type == "all":
        # 查询首页所需的数据并按规定的格式响应回去
        # 轮播图  专辑  文章
        images = TImage.objects.filter(status=1)
        headers = []
        for image in images:
            headers.append({"id": image.pk, "desc": image.title, "thumbnail": str(image.img_url)})
        data = json.dumps({"headers": headers})
        return HttpResponse(data)
    elif type == "wen":
        # 代表范文的是专辑 查询专辑的信息响应回去
        album = TGhosa.objects.all()
        albums = []
        for i in album:
            albums.append(
                {"id": i.pk, "title": i.album_name, "author": i.author, "broadcast": i.broadcast, "set_count": i.number,
                 "grade": str(i.grade), "thumbnail": str(i.album_img)})
        data = json.dumps({"albums": albums})
        return HttpResponse(data)
    elif type == "si":
        if sub_type == "ssyj":
            # 查询属于上师言教的文章
            article = Article.objects.filter(category='上师言教')
            articles = []
            for i in article:
                articles.append({"id": i.pk, "title": i.title, 'author': i.author, "content": str(i.content),
                                 "publish_date": i.publish_date.strftime("%Y-%m-%d")})
            data = json.dumps({"articles": articles})
            return HttpResponse(data)
        else:
            # 查询属于显密法要的文章
            article = Article.objects.filter(category='显密法要')
            articles = []
            for i in article:
                articles.append({"id": i.pk, "title": i.title, 'author': i.author, "content": str(i.content),
                                 "publish_date": i.publish_date.strftime("%Y-%m-%d")})
            data = json.dumps({"articles": articles})
            return HttpResponse(data)


def get_album_chapter(request):
    user_id = request.GET.get("uid")
    album_id = request.GET.get('id')
    if not user_id:
        data = {
            'status': 401,
            'msg': "用户未登陆"
        }
        return HttpResponse(json.dumps(data))

    if album_id:
        detail = TChapter.objects.filter(buddhist_id=album_id)
        details = []
        for i in detail:
            details.append({"id": i.pk, "name": i.chapter, "audio_url": str(i.voice_url), "audio_size": i.memory,
                            "duration": i.duration})
        data = json.dumps({"details": details})
        return HttpResponse(data)


@csrf_exempt
def register(request):
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    salt = str(random.randint(100000, 999999))
    sha = hashlib.sha1()
    sha.update((password+salt).encode())
    password = sha.hexdigest()
    print(phone,password)
    try:
        if TUser.objects.filter(phone=phone).first():
            data = json.dumps({"error": "-200", "error_msg": "该手机号已存在"})
            return HttpResponse(data)
        with transaction.atomic():
            TUser.objects.create(phone=phone, password=password, register_data=time.strftime('%Y-%m-%d'))
        user = TUser.objects.filter(phone=phone, password=password).last()
        data = json.dumps({"uid": user.pk, "phone": user.phone, "password": user.password})
        return HttpResponse(data)
    except:
        return HttpResponse({"data": []})


@csrf_exempt
def edit_user(request):
    user_id = request.POST.get('uid')
    username = request.POST.get('username')
    religious_name = request.POST.get('religious_name')
    password = request.POST.get('password')
    gender = request.POST.get('gender')
    address = request.POST.get('address')
    mail = request.POST.get('email')
    state = request.POST.get('state')
    phone = request.POST.get('phone')
    try:
        user = TUser.objects.filter(pk=user_id).first()
        if user:
            with transaction.atomic():
                if username:
                    user.username = username
                if religious_name:
                    user.fa_name = religious_name
                if password:
                    salt = str(random.randint(100000, 999999))
                    sha = hashlib.sha1()
                    sha.update((password + salt).encode())
                    password = sha.hexdigest()
                    user.password = password
                if gender:
                    user.gender = gender
                if address:
                    user.address = address
                if mail:
                    user.mail = mail
                if state:
                    user.state = state
                if phone:
                    user.phone = phone
                user.save()
            new_user = TUser.objects.get(pk=user_id)
            data = json.dumps({"uid": new_user.pk, "username": new_user.username, "religious_name": new_user.religious_name,
                               "password": new_user.password, "gender": new_user.gender,"address": new_user.address,
                               "mail": new_user.mail, "state": new_user.state, "phone": new_user.phone})
            return HttpResponse(data)
        else:
            return HttpResponse(json.dumps({"error": "-200", "error_msg": "该用户不存在"}))
    except:
        return HttpResponse(json.dumps({"error": "-200", "error_msg": "该用户不存在"}))
