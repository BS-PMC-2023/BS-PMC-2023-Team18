from django.conf.urls import url
from rewear_app import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
]