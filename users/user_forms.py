from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
import sys
import os
from .models import User_Profile

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from orders.models import Location, Location_Info
from orders.locations import get_location_choices

class UserCreationForm(BaseUserCreationForm):
    name = forms.CharField(label="Full Name")
    location_id = forms.ChoiceField(
        label="Hospital Location:",
        help_text="Select an option from the menu above.",
        choices=get_location_choices())

    email = forms.EmailField(
        required=False,
        label="Email",
        help_text = "(not required)" )

    phone = forms.CharField(
        required=False,
        max_length=12,
        label="Mobile Number",
        help_text="(not required)")

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

    def save(self, commit=True, *args, **kwargs):
        user = super(UserCreationForm, self).save(commit=False, *args, **kwargs)
        name = self.cleaned_data["name"]
        if len(name.split()) >= 2:
            user.first_name, user.last_name = (name.split()[0].title(), name.split()[-1].title())
        elif len(name.split()) == 1:
            user.first_name = name.title()
            user.last_name = ""

        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            user.profile.phone = self.cleaned_data["phone"]
            location_id = int(self.cleaned_data["location_id"])
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

class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        email = kwargs.get("instance").email
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.initial["email"] = email
        # self.helper = FormHelper(self)
        # self.helper.add_input(Submit("submit", "Submit", css_class="btn btn-outline-info"))
        # self.helper.form_method = "POST"

    email = forms.EmailField(
        required=False,
        label="Email",
        help_text = "(not required)")

    class Meta:
        model = User
        fields = ["username", "email"]

class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        location_id = kwargs.get("instance").location.location_id
        phone = kwargs.get("instance").phone
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        loc_ids = get_location_choices()
        self.initial["location_id"] = location_id
        self.initial["phone"] = phone
        # self.helper = FormHelper(self)
        # self.helper.add_input(Submit("submit", "Submit", css_class="btn btn-outline-info"))
        # self.helper.form_method = "POST"

    location_id = forms.ChoiceField(
        label="Hospital Location:",
        help_text="Select an option from the menu above.",
        choices=get_location_choices())

    phone = forms.CharField(
        required=False,
        max_length=12,
        label="Mobile Number",
        help_text="(not required)")

    class Meta:
        model = User_Profile
        fields = ["image", "location_id", "phone"]
    def save(self, commit=True, *args, **kwargs):
        profile = super(ProfileUpdateForm, self).save(commit=False, *args, **kwargs)

        if commit:
            profile.save()
            profile.phone = self.cleaned_data["phone"]
            new_location_id = int(self.cleaned_data["location_id"])
            profile.location.delete()
            new_location = Location(
                username = self.instance.user.username,
                location_id = new_location_id,
                info = Location_Info.objects.filter(pk=new_location_id).first()
            )
            new_location.save()
            profile.location = new_location
            profile.save()

        return profile










