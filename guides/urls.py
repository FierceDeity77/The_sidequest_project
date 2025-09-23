from django.urls import path
from . import views

app_name = "guides"

urlpatterns = [
    path("guides-explore/", views.Guides.as_view(), name="guides"),
]
