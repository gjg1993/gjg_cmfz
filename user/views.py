import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render,redirect
from admins.models import TUser
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def get_user(request):
    rows = request.GET.get('rows')
    page = request.GET.get('page', 1)
    users = TUser.objects.all().order_by('id')
    all_page = Paginator(users, rows)
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
        if isinstance(u,TUser):
            return {
                'id': u.id,
                'username': u.username,
                'religious_name': u.religious_name,
                'state': u.state,
                'address': u.address,
                'head_img': str(u.head_img),
                'gender': u.gender,
                'phone': u.phone,
                'mail': u.mail,

            }
    data = json.dumps(page_data, default=my_default)
    return HttpResponse(data)


@csrf_exempt
def add_user(request):
    username = request.POST.get("username")
    religious_name = request.POST.get('religious_name')
    state = request.POST.get('state')
    address = request.POST.get('address')
    head_img = request.FILES.get('head_img')
    gender = request.POST.get('gender')
    phone = request.POST.get('phone')
    mail = request.POST.get('mail')
    result = TUser.objects.create(username=username,
                                  religious_name=religious_name,
                                  state=state,
                                  address=address,
                                  head_img=head_img,
                                  gender=gender,
                                  phone=phone,
                                  mail=mail,
                                  )
    if result:
        return HttpResponse(1)


@csrf_exempt
def edit(request):
    user_id = request.POST.get('id')
    user = TUser.objects.filter(id=user_id)

    def my_default(u):
        if isinstance(u, TUser):
            return {

                'username': u.username,
                'religious_name': u.religious_name,
                'state': u.state,
                'address': u.address,
                'gender': u.gender,
                'phone': u.phone,
                'mail': u.mail,
            }
    return JsonResponse({'data': list(user)}, json_dumps_params={"default": my_default})


@csrf_exempt
def edit_logic(request):
    user_id = request.POST.get('id')
    user = TUser.objects.filter(id=user_id)[0]
    user.username = request.POST.get('username')
    user.religious_name = request.POST.get('religious_name')
    user.state = request.POST.get('state')
    user.address = request.POST.get('address')
    img = request.FILES.get('head_img')
    if img == None:
        user.head_img = user.head_img
    else:

        user.head_img = img
    user.gender = request.POST.get('gender')
    user.phone = request.POST.get('phone')
    user.mail = request.POST.get('mail')
    user.save()
    return HttpResponse(1)


@csrf_exempt
def operate(request):
    option = request.POST.get('oper')
    if option == 'del':
        user_id = request.POST.get('id')
        TUser.objects.get(pk=user_id).delete()
    return HttpResponse('success')


def get_data(request):
    pass