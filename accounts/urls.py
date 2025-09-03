from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.user_login.as_view(), name="login"),
    path("register/", views.register.as_view(), name="register"),
    path("logout/", views.user_logout, name="logout")
]
