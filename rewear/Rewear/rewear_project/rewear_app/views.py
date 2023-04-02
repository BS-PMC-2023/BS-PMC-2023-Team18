from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    attributes = {'key': 'value'}
    return render(request, 'rewear_app/index.html', context=attributes)

def header(request):
    attributes = {}
    return render(request, 'rewear_app/index.html', context=attributes)

# Create your views here.
