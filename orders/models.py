from django.db import models
from django.utils import timezone
from django.contrib.gis.db.models import PointField
from annoying.fields import AutoOneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class User_Profile(models.Model):
    user = AutoOneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name="profile")
    saved_orders = models.ManyToManyField("Order", through="User_Orders")
    location = models.ForeignKey("Location", on_delete=models.CASCADE, related_name="users", null=True)
    # photo = models.ImageField(upload_to="profileimages/", blank=True, null=True)
    phone = models.CharField(max_length=12, help_text="Enter phone number (optional)", blank=True, null=True)
    #class Meta:
        #app_label = "s"

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
    item_type = models.CharField(
        max_length=2,
        choices=TYPE_OPTIONS,
        default=OTHER,
    )
    orders = models.ManyToManyField("Order", blank=True, through="Order_Items")

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(Menu_Item, blank=True, through="Order_Items")
    date_created = models.DateTimeField(default=timezone.now)
    profiles = models.ManyToManyField(User_Profile, through="User_Orders")
    author = models.ForeignKey(User_Profile, on_delete=models.CASCADE, related_name="my_orders")

    def __str__(self):
        string = ""
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
class User_Orders(models.Model):
    user_profile = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

# Explicit through table for order <-> menu_item (ManyToMany)
class Order_Items(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(Menu_Item, on_delete=models.CASCADE)

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
    restr_type = models.CharField(
        max_length=2,
        choices=TYPE_OPTIONS,
        default=OTHER,
    )
    menu_item = models.ForeignKey(Menu_Item, on_delete=models.CASCADE)
    mass_allowed_milligrams = models.FloatField(help_text="Enter quantity allowed (in milligrams)", default=0)

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
        return f"{self.city}, {self.state}: {self.name}"

class Location(models.Model):
    _id = models.AutoField(primary_key=True)
    # used for updating location_info when tchhack locations API is called (old location_info is erased and updated)
    location_id = models.IntegerField(null=True)
    location_info = models.ForeignKey("Location_Info", on_delete=models.SET_NULL, null=True)
    class Meta:
        ordering = ("location_id",)

    def __str__(self):
        if self.location_info is not None:
            return self.location_info.__str__()
        else:
            return "Location info missing, or has not been specified"
    #def set_location(self, loc

