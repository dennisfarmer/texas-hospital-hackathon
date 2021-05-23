from django.db import models
from django.utils import timezone
from django.contrib.gis.db.models import PointField
from django.contrib.auth.models import User

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from users.models import User_Profile

class Menu_Item(models.Model):
    BREAKFAST = "BF"
    LUNCH = "LU"
    DINNER = "DI"
    OTHER = "OT"
    TYPE_OPTIONS = [
        (BREAKFAST, "Breakfast"),
        (LUNCH, "Lunch"),
        (DINNER, "Dinner"),
        (OTHER, "Other/Unspecified")
    ]

    item_id = models.AutoField(primary_key=True)
    name = models.TextField(help_text="Enter the name of the food")
    item_type = models.CharField(max_length=2,
                                 choices=TYPE_OPTIONS,
                                 default=OTHER,)

    orders = models.ManyToManyField("Order",
                                    blank=True,
                                    through="Order_Item")

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    name = models.TextField()
    items = models.ManyToManyField(Menu_Item,
                                   blank=True,
                                   through="Order_Item")

    date_created = models.DateTimeField(default=timezone.now)
    profiles = models.ManyToManyField(User_Profile, through="User_Order")
    author = models.ForeignKey(User_Profile,
                               on_delete=models.CASCADE,
                               related_name="my_orders")

    def __str__(self):
        string = f"{self.name}: "
        if self.items.count():
            for i in self.items.all():
                if i is self.items.last():
                    string = "".join([string, "and ", i, "."])
                else:
                    string = "".join([string, ", ", i, ", "])
        else:
            string = "Order is empty"
        return string

    def __bool__(self):
        return self.items.count() == 0

# Explicit through table for user_profile <-> order (ManyToMany)
class User_Order(models.Model):
    user_profile = models.ForeignKey(User_Profile,
                                     on_delete=models.CASCADE)

    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user_profile.user.username}: {self.order.name}"

# Explicit through table for order <-> menu_item (ManyToMany)
class Order_Item(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE)

    menu_item = models.ForeignKey(Menu_Item,
                                  on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.order.name}: {self.menu_item.name}"

class Dietary_Restriction(models.Model):
    ALLERGIES = "AL"
    CULTURE = "CR"
    CONDITION = "CD"
    OTHER = "OT"
    TYPE_OPTIONS = [
        (ALLERGIES, "Food Allergies"),
        (CULTURE, "Culture/Religion"),
        (CONDITION, "Health Conditions"),
        (OTHER, "Other/Unspecified")
    ]

    restr_id = models.AutoField(primary_key=True)
    name = models.TextField()
    info = models.TextField(default="", blank=True)
    restr_type = models.CharField(max_length=2,
                                  choices=TYPE_OPTIONS,
                                  default=OTHER,)
    menu_item = models.ForeignKey(Menu_Item, on_delete=models.CASCADE)

    mass_allowed_milligrams = models.FloatField(
        help_text="Enter quantity allowed (in milligrams)",
        default=0)

    def __str__(self):
        if self.info:
            if self.mass_allowed_milligrams == 0:
                return f"{self.name} not allowed: {self.info}"
            else:
                return f"{self.name} limited to {self.mass_allowed_milligrams} mg: {self.info}"
        else:
            if self.mass_allowed_milligrams == 0:
                return f"{self.name} not allowed"
            else:
                return f"{self.name} limited to {self.mass_allowed_milligrams} mg"

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
    username = models.CharField(max_length=150,
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

