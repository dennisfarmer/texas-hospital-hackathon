from django import forms
from django.contrib.auth.models import User

# here lies shattered dreams...
#from django.contrib.admin.widgets import FilteredSelectMultiple
#from django_select2.forms import ModelSelect2MultipleWidget
#from searchableselect.widgets import SearchableSelect

#from django.contrib.auth.forms import ucf as base...
import sys, os
from .models import (
    Menu_Item,
    Order,
    Order_Item,
    Order_Purchase,
    MAX_CHARFIELD_LENGTH
)
from .foods import get_food_groups, backup_custom_food

class OrderCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=MAX_CHARFIELD_LENGTH)
    info = forms.CharField(max_length=MAX_CHARFIELD_LENGTH)
    items = forms.ModelMultipleChoiceField(
        label="Items: [Press Ctrl+F to search entries, and End to go to the bottom]",
        # i give up, searchable multichoice is a foggy dream in a distant dreamland
        # (dis shit don't work smdh)
        #widget=FilteredSelectMultiple("Menu_Item", is_stacked=False),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        queryset=Menu_Item.objects.order_by("name"))

    class Media:
        css = {"all": ("/static/admin/css/widgets.css",),}
        js = ("/admin/jsi18n",)

    class Meta:
        model = Order
        #exclude = ("date_created", "author")
        fields = ["name", "info", "items"]

    def save(self, commit=True, *args, **kwargs):
        order = super(OrderCreationForm, self).save(commit=False, *args, **kwargs)
        order_name = self.cleaned_data["name"]
        order_info = self.cleaned_data["info"]
        if commit:
            order.name = order_name
            order.info = order_info
            order.save()
            # establish link to order for each item in order 
            # using through table Order_Item
            for menu_item in self.cleaned_data["items"]:
                Order_Item(order = order,
                           menu_item_name = menu_item.name,
                           menu_item = menu_item).save()
            order.save()
        return order

class MenuItemCreationForm(forms.ModelForm):
    # should automatically be implemented 
    # by forms.ModelForm using the model definition:
    name = forms.CharField(max_length=MAX_CHARFIELD_LENGTH)
    food_group = forms.ChoiceField(
        choices=[(g,g) for g in get_food_groups()],
        initial="Unclassified")
    class Meta:
        model = Menu_Item
        fields = ["name", "food_group"]

    def save(self, commit=True, *args, **kwargs):
        item = super(MenuItemCreationForm, self).save(commit=False,
                                                   *args,
                                                   **kwargs)
        name = self.cleaned_data["name"]
        food_group = self.cleaned_data["food_group"]
        if commit:
            item.name = name
            item.food_group = food_group
            item.save()
            # backup custom food items to csv
            backup_custom_food(item.pk, name, food_group)
        return item

class PlaceOrderForm(forms.ModelForm):
    class Meta(self):
        model = Order_Purchase
        fields = ["vendor"]

class OrderUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        order = kwargs.get("instance")
        super(OrderUpdateForm, self).__init__(*args, **kwargs)
        self.initial["items"] = (
            Menu_Item.objects.filter(orders=order))

    name = forms.CharField(max_length=MAX_CHARFIELD_LENGTH)
    info = forms.CharField(max_length=MAX_CHARFIELD_LENGTH)
    #items = forms.ChoiceField(label = "Menu Items",
                                  #queryset = Menu_Item.objects.all(),
                                  #widget=ModelSelect2MultipleWidget(
                                      #model=Menu_Item,
                                      #search_fields=["name__icontains"]
                                  #)
                                  #required = False
                                  #)
    class Meta:
        model = Order
        fields = ["name", "info", "items"]

    def save(self, commit=True, *args, **kwargs):
        order = super(OrderUpdateForm, self).save(commit=False, *args, **kwargs)
        order_name = self.cleaned_data["name"]
        order_info = self.cleaned_data["info"]
        if commit:
            order.name = order_name
            order.info = order_info
            order.save()
            # refresh the Order_Item entries by dropping the old
            # entries and creating new ones
            Order_Item.objects.filter(order=order).delete()
            for menu_item in self.cleaned_data["items"]:
                Order_Item(order = order,
                           menu_item_name = menu_item.name,
                           menu_item = menu_item).save()
            order.save()
        return order

