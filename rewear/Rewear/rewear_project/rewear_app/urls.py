from django.urls import re_path, path
from rewear_app import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]