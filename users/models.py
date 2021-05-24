from django.db import models
from django.contrib.auth.models import User
#from annoying.fields import AutoOneToOneField
from PIL import Image

class User_Profile(models.Model):
    user = models.OneToOneField(User,
                                primary_key=True,
                                on_delete=models.CASCADE,
                                related_name="profile")

    #saved_orders=models.ManyToManyField("orders.Order", through="orders.User_Order")

    location=models.OneToOneField("orders.Location",
                               on_delete=models.CASCADE,
                               related_name="user_profile",
                               help_text="(do not change)",
                               null=True)

    image = models.ImageField(upload_to="users/profileimages/",
                              default="users/default.jpg")

    phone = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

