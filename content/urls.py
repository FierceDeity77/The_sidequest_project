from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("reviews/", views.Reviews.as_view(), name="reviews"),
    path("guides/", views.Guides.as_view(), name="guides"),

    path("communities/", views.CommunityList.as_view(), name="communities"),
    path("communities/<slug:slug>/", views.CommunityDetail.as_view(), name="community-detail"),
    path("create-subcommunity/<slug:slug>/", views.CreateSubCommunity.as_view(), name="create-subcommunity"),

    path("games/", views.Games.as_view(), name="game-list"),
    path("add-game/", views.AddGame.as_view(), name="add-game"),
    path("game-detail/<slug:slug>/", views.GameDetail.as_view(), name="game-detail"),
    
    path("create-topic/<slug:slug>/", views.CreateTopic.as_view(), name="create-topic"),
    path("topic/<slug:slug>/", views.TopicDetail.as_view(), name="topic-detail"),
    path("topic/<slug:slug>/comment/", views.AddComment.as_view(), name="add-comment"), # set to same url but changed the views for post
    path("topic/<slug:slug>/comment/<int:parent_id>/", views.AddComment.as_view(), name="add-comment"), # comment for community that has a parent (sub-community)
    
]
