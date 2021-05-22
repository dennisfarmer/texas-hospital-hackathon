from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="orders-home"),
    path("about/", views.about, name="orders-about"),
    #path("my_orders/", views.my_orders, name="orders-my_orders"),
    #path("saved_orders/", views.saved_orders, name="orders-saved_orders"),
]
