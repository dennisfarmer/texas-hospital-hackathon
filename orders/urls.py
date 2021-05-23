from django.urls import path
from .views import PostListView, PostDetailView
from . import views

urlpatterns = [
    path("", PostListView.as_view(), name="orders-home"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="order-detail"),
    path("about/", views.about, name="orders-about"),
    #path("my_orders/", views.my_orders, name="orders-my_orders"),
    #path("saved_orders/", views.saved_orders, name="orders-saved_orders"),
]
