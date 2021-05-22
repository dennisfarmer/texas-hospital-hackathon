from django import forms
from django.contrib.auth.models import User
import sys
import os
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from orders.models import User_Profile, Location, Location_Info
from orders.locations import get_location_choices

class UserCreationForm(BaseUserCreationForm):
    location_id = forms.ChoiceField(label="Hospital Location:", choices=get_location_choices())
    email = forms.EmailField(required=False, label="Email (not required): ")
    phone = forms.CharField(required=False, label="Phone number (not required):", max_length=12)

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "location_id",
            "email",
            "phone"
        ]

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
            location_id = self.cleaned_data["location_id"]
            user_loc = Location(
                location_id = location_id,
                location_info = Location_Info.objects.filter(pk=location_id).first()
            ).save()
            user.profile.location = user_loc
            user.profile.phone = self.cleaned_data["phone"]
            user.profile.save()

        return user

