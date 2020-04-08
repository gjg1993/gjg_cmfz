from django.shortcuts import render
from admins.models import TImage
# Create your views here.

def get_banner(request):
    rows = request.GET.get('rows')
    page = request.GET.get('page')



