from django.shortcuts import render
from .models import Order

# TODO: write a "My Orders" page that uses most of the code from
# "Saved Orders", with the option to edit orders (add check to see if
# current user is equal to author of order, etc)

def home(request):
    context = {
        "orders": Order.objects.all()
    }
    return render(request, "orders/home.html", context)

def about(request):
    return render(request, "orders/about.html", {"title": "About"})

