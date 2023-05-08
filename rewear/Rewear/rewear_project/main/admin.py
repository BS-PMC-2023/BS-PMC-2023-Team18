from django.contrib import admin
# from .models import ToDoList, Item
# from .models import HostingPlace, GuideInfo
from main.models import market, submission, myEvent, Message
# Register your models here.
# admin.site.register(ToDoList)
# admin.site.register(Item)
# here admin can edit the market
admin.site.register(market)
admin.site.register(submission)
admin.site.register(myEvent)
# admin.site.register(HostingPlace)
# admin.site.register(GuideInfo)
admin.site.register(Message)