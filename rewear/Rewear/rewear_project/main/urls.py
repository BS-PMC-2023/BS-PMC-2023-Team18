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
path("search_page/", views.search_page, name="search"),
path("market_page/<id>/", views.market_page, name="market"),
path("update_market/<id>/", views.update_market, name="update_market"),
path("submissions/", views.submissions, name="submissions"),
path("submit_request/<uid>/<mid>/", views.submit_request, name="submit_request"),
path("feedback/<id>/", views.feedback, name="feedback"),
]