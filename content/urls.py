from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("reviews/", views.Reviews.as_view(), name="reviews"),
    path("guides/", views.Guides.as_view(), name="guides"),
    path("discussions/", views.Discussions.as_view(), name="discussions"),
    path("explore/", views.Explore.as_view(), name="explore"),
    path("communities/", views.CommunityList.as_view(), name="communities"),
    path("communities/<slug:slug>/", views.CommunityDetail.as_view(), name="community-detail"),
    path("add-game/", views.AddGame.as_view(), name="add-game"),
    path("create-subcommunity/<slug:slug>/", views.CreateSubCommunity.as_view(), name="create-subcommunity"),
    path("create-topic/<slug:slug>/", views.CreateTopic.as_view(), name="create-topic"),
    path("topic/<slug:slug>/", views.TopicDetail.as_view(), name="topic-detail"),
    path("topic/<slug:slug>/comment/", views.AddComment.as_view(), name="add-comment"), # set to same url but changed the views for post
    path("topic/<slug:slug>/comment/<int:parent_id>/", views.AddComment.as_view(), name="add-comment"),
]
