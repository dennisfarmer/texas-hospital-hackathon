from django.db.models.signals import post_save
from django.db.utils import OperationalError
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import User_Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            User_Profile.objects.create(user=instance)
        except OperationalError as err:
            print("django.db.utils.OperationalError: ", err, "\nsignals.py: Nonfatal error...", sep="")
            pass

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except OperationalError as err:
        print("django.db.utils.OperationalError: ", err, "\nsignals.py: Nonfatal error...", sep="")
        pass
