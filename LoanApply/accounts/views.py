from django.shortcuts import render
from accounts.forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

# Create your views here.

def signup(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signed Up Successfully!!!')
            return HttpResponseRedirect(reverse("accounts:login"))
        
    diction = {"title": "SignUp Form", "form": form, 'title': "signup page"}
    return render(request, "accounts/signup.html", context=diction)


def loginview(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You logged into your account")
                return HttpResponseRedirect(reverse("home:homely"))
            else:
                messages.error(request, "Entered Details are incorrect!!!")
    diction = {"form": form, "title":"Login Form", 'title': "login page"}
    return render(request, "accounts/login.html", context=diction)


@login_required
def loggedout(request):
    logout(request)
    messages.warning(request, "You logged out!!!")
    return HttpResponseRedirect(reverse("home:homely"))


@login_required
def change_pwd(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == "POST":
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
            messages.success(request, "Password changed successfully!!!")
            return HttpResponseRedirect(reverse("accounts:login"))
        else:
            messages.warning(request, "Something went wrong!!!")
            
    diction = {"form": form, "changed":changed, 'title': "password change"}
    return render(request, "accounts/change_password.html", context=diction)

