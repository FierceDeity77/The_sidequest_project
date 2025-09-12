from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.user_login.as_view(), name="login"),
    path("register/", views.register.as_view(), name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/<str:email>/", views.ProfileView.as_view(), name="user-profile"),
]
