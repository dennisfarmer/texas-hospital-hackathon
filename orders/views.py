from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Order

# TODO: write a "My Orders" page that uses most of the code from
# "Saved Orders", with the option to edit orders (add check to see if
# current user is equal to author of order, etc)

def home(request):
    context = {
        "orders": Order.objects.all()
    }
    return render(request, "orders/home.html", context)

class OrderListView(ListView):
    model = Order
    template_name = "order/home.html"
    context_object_name = "orders"
    ordering = ["-date_created"]

class OrderDetailView(DetailView):
    model = Order

def about(request):
    return render(request, "orders/about.html", {"title": "About"})

