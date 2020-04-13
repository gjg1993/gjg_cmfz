import json
from mutagen.mp3 import MP3
from django.db import transaction
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from admins.models import TGhosa,TChapter
# Create your views here.


def get_album(request):
    rows = request.GET.get('rows')
    page = request.GET.get('page', 1)
    albums = TGhosa.objects.all().order_by('id')
    all_page = Paginator(albums, rows)
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
        if isinstance(u, TGhosa):
            return {
                'id': u.id,
                'album_name': u.album_name,
                'grade': str(u.grade),
                'author': u.author,
                'broadcast': u.broadcast,
                'number': u.number,
                'intro': u.intro,
                'issue_data': u.issue_data.strftime('%Y-%m-%d'),
                'upload_data': u.upload_data.strftime('%Y-%m-%d'),
                'status': u.status,
                'album_img': str(u.album_img)
            }
    data = json.dumps(page_data,default=my_default)
    return HttpResponse(data)


def get_chapter(request):
    album_id = request.GET.get('albumId')
    page = request.GET.get('page')
    rows = request.GET.get('rows')
    albums = TChapter.objects.filter(buddhist=album_id).order_by('id')
    all_page = Paginator(albums, rows)
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
        if isinstance(u,TChapter):
            return {
                'buddhist': u.buddhist_id,
                'id': u.id,
                'chapter': u.chapter,
                'memory': u.memory,
                'duration': u.duration,
                'voice_url': str(u.voice_url),
            }
    data = json.dumps(page_data,default=my_default)
    return HttpResponse(data)


@csrf_exempt
def operate(request):
    try:
        option = request.POST.get('oper')
        if option == 'add':
            album_name = request.POST.get('album_name')
            grade = request.POST.get('grade')
            author = request.POST.get('author')
            broadcast = request.POST.get('broadcast')
            number = request.POST.get('number')
            intro = request.POST.get('intro')
            status = request.POST.get('status')
            issue_data = request.POST.get('issue_data')
            upload_data = request.POST.get('upload_data')
            album_img = request.POST.get('album_img')
            with transaction.atomic():
                TGhosa.objects.create(album_name=album_name, grade=grade, author=author, broadcast=broadcast, number=number, intro=intro, status=status, issue_data=issue_data,upload_data=upload_data, album_img=album_img.split("\\")[-1])
        elif option == 'edit':
            id = request.POST.get('id')
            album = TGhosa.objects.filter(pk=id)[0]
            with transaction.atomic():
                album.album_name = request.POST.get('album_name')
                album.grade = request.POST.get('grade')
                album.author = request.POST.get('author')
                album.broadcast = request.POST.get('broadcast')
                album.number = request.POST.get('number')
                album.intro = request.POST.get('intro')
                album.status = request.POST.get('status')
                album.issue_data = request.POST.get('issue_data')
                album.upload_data = request.POST.get('upload_data')
                album_img = request.POST.get('album_img')
                if album_img:
                    album.album_img = album_img.split("\\")[-1]
                else:
                    album.album_img = album.album_img
                album.save()
        elif option == 'del':
            id = request.POST.get('id')
            with transaction.atomic():
                TGhosa.objects.filter(pk=id)[0].delete()
        return HttpResponse(1)
    except:
        return HttpResponse(0)


@csrf_exempt
def add_chapter(request):
    try:
        chapter = request.POST.get('chapter')
        album_id = request.POST.get('album_id')
        voice_url= request.FILES.get('voice_url')
        print(chapter, album_id, voice_url)
        if voice_url:
            size = voice_url.size
            m = int(size) / (1024 * 1024)
            memory = str('%.1f' % m) + 'M'
            mp3 = MP3(voice_url)
            time = mp3.info.length
            minutes = int(time) // 60
            seconds = int(time) % 60
            duration = str(minutes) + '分' + str(seconds) + '秒'
            with transaction.atomic():
                result = TChapter.objects.create(chapter=chapter, voice_url=voice_url,memory=memory,duration=duration,buddhist_id=album_id)
                if result:
                    album = TGhosa.objects.filter(pk=album_id)[0]
                    album.number = album.number + 1
                    album.save()
                return HttpResponse(1)
    except:
        return HttpResponse(0)


def get_chapter_name(request):
    id = request.GET.get('id')
    chapter = TChapter.objects.get(id=id)

    def my_default(u):
        if isinstance(u, TChapter):
            return {'chapter': u.chapter}
    return JsonResponse(chapter, safe=False, json_dumps_params={'default': my_default})


def del_chapter(request):
    try:
        id = request.GET.get('id')
        with transaction.atomic():
            chapter = TChapter.objects.filter(pk=id)[0]
            result = chapter.delete()
            if result:
                album = TGhosa.objects.filter(pk=chapter.buddhist_id)[0]
                album.number = album.number-1
                album.save()
                return HttpResponse(1)
    except:
        return HttpResponse(0)


@csrf_exempt
def edit_chapter(request):
    try:
        id = request.POST.get('id')
        chapter_name = request.POST.get('chapter')
        voice_url = request.FILES.get('voice_url')
        chapter = TChapter.objects.filter(pk=id)[0]
        with transaction.atomic():
            chapter.chapter = chapter_name
            if voice_url:
                size = voice_url.size
                m = int(size) / (1024 * 1024)
                memory = str('%.1f' % m) + 'M'
                mp3 = MP3(voice_url)
                time = mp3.info.length
                minutes = int(time) // 60
                seconds = int(time) % 60
                duration = str(minutes) + '分' + str(seconds) + '秒'
                chapter.voice_url = voice_url
                chapter.memory = memory
                chapter.duration = duration
            else:
                chapter.voice_url = chapter.voice_url
                chapter.memory = chapter.memory
                chapter.duration = chapter.duration
            chapter.save()
            return HttpResponse(1)
    except:
        return HttpResponse(0)


























