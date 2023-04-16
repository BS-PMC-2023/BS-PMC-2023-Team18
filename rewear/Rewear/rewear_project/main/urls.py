from django.urls import path, include

from . import views

urlpatterns = [
path("", views.home, name="home"),
path("about/", views.about, name="about"),
path("areyousure/", views.areyousure, name="areyousure"),
path("profile/<username>", views.profile, name="profile"),
path("profile/", views.myprofile, name="myprofile"),
path("messagetouser/<username>", views.messagetouser, name="messagetouser"),
path("sendmessage/<username>", views.sendmessage, name="sendmessage"),
path("editabout/", views.editabout, name="editabout"),
path("saveabout/", views.saveabout, name="saveabout"),
path("search/", views.search, name="search"),
]