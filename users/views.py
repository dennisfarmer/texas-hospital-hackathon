from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from .user_forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            # change this v v v
            messages.success(request, f"Account created for {username}")
            return redirect("orders-home")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

