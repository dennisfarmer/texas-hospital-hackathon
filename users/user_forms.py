from django import forms
from django.contrib.auth.models import User
import sys
import os
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from orders.models import User_Profile, Location, Location_Info
from orders.locations import get_location_choices

class UserCreationForm(BaseUserCreationForm):
    name = forms.CharField(label="Full Name")
    location_id = forms.ChoiceField(label="Hospital Location:", help_text="Select an option from the menu above.", choices=get_location_choices())
    email = forms.EmailField(required=False, label="Email", help_text = "(not required)" )
    phone = forms.CharField(required=False, max_length=12, label="Mobile Number", help_text="(not required)") #label="Phone number (not required):"

    class Meta:
        model = User
        fields = [
            "name",
            "username",
            "password1",
            "password2",
            "location_id",
            "email",
            "phone"
        ]

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        name = self.cleaned_data["name"]
        if len(name.split()) >= 2:
            user.first_name, user.last_name = (name.split()[0], name.split()[-1])
        elif len(name.split()) == 1:
            user.first_name = name.split()[0]
            user.last_name = ""

        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            user.profile.phone = self.cleaned_data["phone"]
            location_id = self.cleaned_data["location_id"]
            loc = Location(
                username = user.username,
                location_id = location_id,
                info = Location_Info.objects.filter(pk=location_id).first()
            )
            loc.save()
            user.profile.location = loc
            user.profile.save()
            user.save()

        return user

