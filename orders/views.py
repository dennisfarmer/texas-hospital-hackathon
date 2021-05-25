from django.shortcuts import render
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView

)
from .models import Order, Menu_Item, Order_Purchase
from .order_forms import (
    OrderCreationForm,
    MenuItemCreationForm,
    OrderUpdateForm,
    PlaceOrderForm
)

# TODO: write a "My Orders" page that uses most of the code from
# "Saved Orders", with the option to edit orders (add check to see if
# current user is equal to author of order, etc)

def home(request):
    context = {
        "orders": Order.objects.all()
    }
    return render(request, "orders/home.html", context)

class PlaceOrderSelectView(ListView):
    model = Order
    template_name = "orders/place_order_select.html"
    context_object_name = "orders"
    ordering = ["-date_created"]

# uses update view without updating to access order attrs
class PlaceOrderConfirmView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = PlaceOrderForm
    #context_object_name = "Order"
    # Specifying both fields and form_class is not permitted
    #fields = ['name', 'info', 'items']
    def form_valid(self, form):
        form.instance.customer = self.request.user.profile
        return super().form_valid(form)
    template_name = "orders/place_order_confirm.html"
    success_url = "/"

    def test_func(self):
        order = self.get_object()
        return self.request.user.profile == order.author

class OrderListView(ListView):
    model = Order
    template_name = "orders/home.html"
    context_object_name = "orders"
    ordering = ["-date_created"]

class OrderDetailView(DetailView):
    model = Order
    context_object_name = "order"

# LoginRequiredMixin redirects user to login page if they
# attempt to create order without login
class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreationForm
    #context_object_name = "Order"
    # Specifying both fields and form_class is not permitted
    #fields = ['name', 'info', 'items']
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

class MenuItemCreateView(LoginRequiredMixin, CreateView):
    model = Menu_Item
    form_class = MenuItemCreationForm
    template_name = "orders/item_form.html"
    success_url = "/"
    #context_object_name = "Order"
    # Specifying both fields and form_class is not permitted
    #fields = ['name', 'info', 'items']
    #def form_valid(self, form):
        #form.instance.author = self.request.user.profile
        #return super().form_valid(form)

class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = OrderUpdateForm
    #context_object_name = "Order"
    # Specifying both fields and form_class is not permitted
    #fields = ['name', 'info', 'items']
    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user.profile == order.author

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    context_object_name = "order"
    success_url = "/"

    def test_func(self):
        order = self.get_object()
        return self.request.user.profile == order.author

def about(request):
    return render(request, "orders/about.html", {"title": "About"})

