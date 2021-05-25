from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    MenuItemCreateView,
    OrderUpdateView,
    OrderDeleteView
)
from . import views

urlpatterns = [
    path("", OrderListView.as_view(), name="orders-home"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("order/new/", OrderCreateView.as_view(), name="order-create"),
    path("item/new/", MenuItemCreateView.as_view(), name="item-create"),
    path("order/<int:pk>/update/", OrderUpdateView.as_view(), name="order-update"),
    path("order/<int:pk>/delete/", OrderDeleteView.as_view(), name="order-delete"),
    path("about/", views.about, name="orders-about"),
    path("placeorder/select/", PlaceOrderSelectView.as_view(), name="place-order-select"),
    path("placeorder/<int:pk>/", PlaceOrderConfirmView.as_view(), name="place-order-confirm"),
    #path("my_orders/", views.my_orders, name="orders-my_orders"),
    #path("saved_orders/", views.saved_orders, name="orders-saved_orders"),
]
