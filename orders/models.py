from django.db import models
from django.utils import timezone
from django.contrib.gis.db.models import PointField
from django.contrib.auth.models import User
from django.urls import reverse

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from users.models import User_Profile

MAX_CHARFIELD_LENGTH = 240

class Menu_Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(help_text="Enter the name of the food",
                            max_length=MAX_CHARFIELD_LENGTH)
    food_group = models.CharField(blank=True,
                                  max_length=MAX_CHARFIELD_LENGTH)
    orders = models.ManyToManyField("Order",
                                    blank=True,
                                    through="Order_Item")

    def as_dict(self):
        return {self.name: {
            "item_id": self.item_id,
            "name": self.name,
            "food_group": self.food_group
        }}

    def __str__(self):
        return self.name

    @property
    def display(self):
        if self.food_group != "":
            return f"{self.food_group} - {self.name}"
        else:
            return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
    info = models.CharField(max_length=MAX_CHARFIELD_LENGTH,
                            blank=True, null=True)
    items = models.ManyToManyField(Menu_Item,
                                   blank=True,
                                   through="Order_Item")

    date_created = models.DateTimeField(default=timezone.now)
    #profiles = models.ManyToManyField(User_Profile, through="User_Order")
    author = models.ForeignKey(User_Profile,
                               on_delete=models.CASCADE,
                               related_name="my_orders")

    def __str__(self):
        string = f"{self.name}: "
        if self.items.count():
            for item in self.items.all():
                if item == self.items.last():
                    string = "".join([string, "and ", item, "."])
                else:
                    string = "".join([string, ", ", item, ", "])
        else:
            string = "Order is empty"
        return string

    # display first five items
    @property
    def display_head(self):
        # (cannot pass parameters into jinja object property)
        max_display = 5
        count = self.items.count()
        first = self.items.first()
        last = self.items.last()
        if first is not None:
            for item in self.items.all()[:max_display]:
                if item == first:
                    string = str(first)
                elif item == last:
                    string = "".join([string, ", and ", str(item)])
                else:
                    string = "".join([string, ", ", str(item)])
            if item != last and count > max_display:
                if count - max_display == 1:
                    string = "".join([string, " and 1 other"])
                else:
                    string = "".join([string, " and ",
                                      str(count - max_display),
                                      " others"])
        else:
            string = "Order is empty"
        return string

    def __bool__(self):
        return self.items.count() != 0

    def get_absolute_url(self):
        return reverse("order-detail", kwargs={"pk": self.pk})

class Order_Purchase(models.Model):
    # TODO: instead of models.PROTECT, use a signal to create a copy
    # of orders/customers who have an order in progress / still in the
    # database. For demonstration purposes this works
    customer = models.ForeignKey(User_Profile,
                                on_delete=models.PROTECT
                                )
    order = models.ForeignKey(Order,
                               on_delete=models.PROTECT
                              )
    time_created = models.DateTimeField(default=timezone.now)
    vendor = models.CharField()
    is_fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.user.username}: {self.order.name}"


# Explicit through table for user_profile <-> order (ManyToMany)
#class User_Order(models.Model):
    #user_profile = models.ForeignKey(User_Profile,
                                     #on_delete=models.CASCADE)

    #order = models.ForeignKey(Order,
                              #on_delete=models.CASCADE)
    #def __str__(self):
        #return f"{self.user_profile.user.username}: {self.order.name}"

# Explicit through table for order <-> menu_item (ManyToMany)
class Order_Item(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE)

    menu_item_name = models.CharField(max_length=MAX_CHARFIELD_LENGTH)
    menu_item = models.ForeignKey(Menu_Item,
                                  on_delete=models.SET_NULL,
                                  null=True)
    def __str__(self):
        return f"{self.order.name}: {self.menu_item.name}"

#class Dietary_Restriction(models.Model):
    #ALLERGIES = "AL"
    #CULTURE = "CR"
    #CONDITION = "CD"
    #OTHER = "OT"
    #TYPE_OPTIONS = [
        #(ALLERGIES, "Food Allergies"),
        #(CULTURE, "Culture/Religion"),
        #(CONDITION, "Health Conditions"),
        #(OTHER, "Other/Unspecified")
    #]

    #restr_id = models.AutoField(primary_key=True)
    #name = models.TextField()
    #info = models.TextField(default="", blank=True)
    #restr_type = models.CharField(max_length=2,
                                  #choices=TYPE_OPTIONS,
                                  #default=OTHER,)
    #menu_item = models.ForeignKey(Menu_Item, on_delete=models.CASCADE)

    #mass_allowed_milligrams = models.FloatField(
        #help_text="Enter quantity allowed (in milligrams)",
        #default=0)

    #def __str__(self):
        #if self.info:
            #if self.mass_allowed_milligrams == 0:
                #return f"{self.name} not allowed: {self.info}"
            #else:
                #return f"{self.name} limited to {self.mass_allowed_milligrams} mg: {self.info}"
        #else:
            #if self.mass_allowed_milligrams == 0:
                #return f"{self.name} not allowed"
            #else:
                #return f"{self.name} limited to {self.mass_allowed_milligrams} mg"

class Location_Info(models.Model):
    location_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    address = models.TextField()
    city = models.TextField()
    state = models.TextField()
    zipcode = models.TextField()
    latlong = PointField()
    campus = models.TextField()
    photo_url = models.URLField()
    phone = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f"{self.city}, {self.state} - {self.name}"

class Location(models.Model):
    _id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=MAX_CHARFIELD_LENGTH,
                                help_text="(do not change)")
    # used for updating location_info when tchhack
    # locations API is called (old location_info is 
    # erased and updated)
    location_id = models.IntegerField(null=True,
                                      help_text="(do not change)")

    info = models.ForeignKey("Location_Info",
                             on_delete=models.SET_NULL,
                             null=True,
                             help_text="(do not change)")

    class Meta:
        ordering = ("location_id",)

    # Do not allow editing of the location table except by location_update scripts
    # (to change user_profile location, create a new location entry)
    def save(self, *args, **kwargs):
        if self.pk is None or self.location_info is None:
            super(Location, self).save(*args, **kwargs)

    def __str__(self):
        if self.info is not None:
            return f"{str(self.username)}: {self.info.__str__()}"
        else:
            return "Location info missing, or has not been specified"

    @property
    def display(self):
        if self.info is not None:
            return f"{self.info.name} - {self.info.city}, {self.info.state}"
        else:
            return ""

