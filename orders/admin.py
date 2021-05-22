from django.contrib import admin
from django.apps import apps
from .models import *

#admin.site.register(apps.all_models["orders"].values())
admin.site.register(User_Profile)
admin.site.register(Menu_Item)
admin.site.register(Order)
admin.site.register(User_Orders)
admin.site.register(Order_Items)
admin.site.register(Dietary_Restriction)
admin.site.register(Location_Info)
admin.site.register(Location)


