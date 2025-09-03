from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.views import View



class user_login(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, "accounts/login.html", {"login_form": login_form})
    

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get("email")
            password = login_form.cleaned_data.get("password")
            user = authenticate(request, email=email, password=password) # django authenticates under the hood
            if user is not None:
                login(request, user)  # like Flask's login_user logs the user if credentials is correct
                messages.success(request, "Welcome Back!")
                return redirect("content:home")
            else:
                messages.error(request, "Invalid username or password")
        return render(request, "accounts/login.html", {"login_form": login_form})



class register(View):
    def get(self, request):
        reg_form = RegisterForm()
        return render(request, "accounts/register.html", {"reg_form": reg_form})
    

    def post(self, request):
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid(): # run django's validation
            user = reg_form.save(commit=False) # commit false doesn't save it yet this allows you to modify fields before saving
            # Force all new signups to be normal users
            user.role = "user" # assign custom role field
            user.save() # saves into the database the assign role
            login(request, user)  # Auto login after registration

            messages.success(request, "Account created successfully!")
            return redirect("content:home")
        
        return render(request, "accounts/register.html", {"reg_form": reg_form})



def user_logout(request):
    logout(request)  # like Flask's logout_user
    return redirect("content:home")