from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("reviews-explore/", views.Reviews.as_view(), name="reviews"),
]
