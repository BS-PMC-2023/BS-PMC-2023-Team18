from django.conf.urls import url
from rewear_app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]