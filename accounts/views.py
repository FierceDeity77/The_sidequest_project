from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, ProfileForm
from .models import CustomUser
from django.contrib import messages
from django.views import View
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from content.views.mixins import PaginationMixin
from django.urls import reverse_lazy


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
            user.content_type = "User" # assign content type field
            user.save() # saves into the database the assign role
            login(request, user)  # Auto login after registration

            messages.success(request, "Account created successfully!")
            return redirect("content:home")
        
        return render(request, "accounts/register.html", {"reg_form": reg_form})
    

class ProfileView(LoginRequiredMixin, View, PaginationMixin):
    def get(self, request, id):
        view_user = get_object_or_404(CustomUser, pk=id)
        profile_form = ProfileForm(instance=view_user)
        # Paginate user posts
        # Call paginate_queryset from PaginationMixin and pass the querysets
        list_of_posts = self.paginate_queryset(view_user.user_topics.all().order_by("-created_at"), per_page=5, page_param="posts_page")
        list_of_comments = self.paginate_queryset(view_user.comments.all().order_by("-created_at"), per_page=5, page_param="comments_page")
        list_of_communites = self.paginate_queryset(view_user.joined_communities.all().order_by("-created_at"), per_page=5, page_param="communities_page")
        list_of_games = self.paginate_queryset(view_user.joined_games.all().order_by("-created_at"), per_page=5, page_param="games_page")
        tab = request.GET.get("tab", "posts") # default to posts tab if no tab is specified
        # Pass the tab variable to the template to maintain the active tab state
        # Page links will include ?tab=comments or ?tab=communities etc
        return render(request, "accounts/user_profile.html", {"user_profile": view_user,
                                                              "profile_form": profile_form,
                                                              "list_of_posts": list_of_posts,
                                                              "list_of_comments": list_of_comments,
                                                              "list_of_communities": list_of_communites,
                                                              "list_of_games": list_of_games,
                                                              "tab": tab
                                                              })
    

    def post(self, request, id):
        view_user = get_object_or_404(CustomUser, pk=id)
        profile_form = ProfileForm(request.POST, request.FILES, instance=view_user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("user-profile", id=view_user.id)
        return render(request, "accounts/user_profile.html", {"user_profile": view_user,
                                                              "profile_form": profile_form})


class UserLogoutView(RedirectView):
    url = reverse_lazy("content:home")  # where to redirect after logout

    def get(self, request, *args, **kwargs):
        logout(request)  # clear session
        return super().get(request, *args, **kwargs)