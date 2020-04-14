import json
from django.db import transaction
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render,redirect
from admins.models import TImage
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def get_banner(request):
    rows = request.GET.get('rows')
    page = request.GET.get('page',1)
    images = TImage.objects.all().order_by('id')
    all_page = Paginator(images, rows)
    try:
        page_obj = all_page.page(page).object_list
    except EmptyPage:
        page_obj = all_page.page(int(page)-1).object_list
    page_data = {
        'page': page,
        'total': all_page.num_pages,
        'records': all_page.count,
        'rows': list(page_obj)
    }

    def my_default(u):
        if isinstance(u, TImage):
            return {
                'id': u.id,
                'img_url': str(u.img_url),
                'title': u.title,
                'status': u.status,
                'upload_time' :u.upload_time.strftime('%Y-%m-%d')
            }
    data = json.dumps(page_data, default=my_default)
    return HttpResponse(data)


@csrf_exempt
def add_banner(request):
    try:
        title = request.POST.get("title")
        status = request.POST.get('status')
        pic = request.FILES.get('pic')
        with transaction.atomic():
            result = TImage.objects.create(title=title,status=status,img_url=pic)
            return HttpResponse(1)
    except:
        return HttpResponse(0)



@csrf_exempt
def operate(request):
    try:
        option = request.POST.get('oper')
        if option == 'del':
            img_id = request.POST.get('id')
            with transaction.atomic():
                TImage.objects.get(pk=img_id).delete()
                return HttpResponse('success')
    except:
        return HttpResponse(0)



@csrf_exempt
def edit(request):
    img_id = request.POST.get('id')
    img = TImage.objects.filter(id=img_id)

    def my_default(u):
        if isinstance(u, TImage):
            return {
                'id': u.id,
                'title': u.title,
                'status': u.status,
            }
    return JsonResponse({'data': list(img)}, json_dumps_params={"default": my_default})


@csrf_exempt
def edit_logic(request):
    try:
        id = request.POST.get('id')
        img = TImage.objects.filter(id=id)[0]
        with transaction.atomic():
            img.title = request.POST.get('title')
            img.status = request.POST.get('status')
            img.save()
            return HttpResponse(1)
    except:
        return HttpResponse(0)



