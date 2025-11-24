from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),

    path("community-list/", views.CommunityList.as_view(), name="hubs"),
    path("tavern-list/", views.SubcommunityList.as_view(), name="taverns"),
    path("h/<slug:slug>/", views.CommunityDetail.as_view(), name="community-detail"),
    path("edit-community/<slug:slug>/", views.EditCommunity.as_view(), name="edit-community"),
    
    path("t/<slug:slug>/", views.CommunityDetail.as_view(), name="subcommunity-detail"),
    path("create-subcommunity/<slug:slug>/", views.AddSubCommunity.as_view(), name="create-subcommunity"),

    path("game-list/", views.Games.as_view(), name="game-list"),
    path("add-game/", views.AddGame.as_view(), name="add-game"),
    path("g/<slug:slug>/", views.GameDetail.as_view(), name="game-detail"),
    
    path("create-topic/<slug:slug>/", views.AddTopic.as_view(), name="create-topic"),
    path("topic/<slug:slug>/", views.TopicDetail.as_view(), name="topic-detail"),
    path("topic/<slug:slug>/comment/", views.AddComment.as_view(), name="add-comment"), # set to same url but changed the views for post
    path("topic/<slug:slug>/comment/<int:parent_id>/", views.AddComment.as_view(), name="add-comment"), # comment for community that has a parent (sub-community)
    path("topic-delete/<slug:slug>/", views.DeleteTopic.as_view(), name="delete-topic"),
    path("topic-edit/<slug:slug>/", views.EditTopic.as_view(), name="edit-topic"),

    path("comment-delete/<int:id>/", views.DeleteComment.as_view(), name="delete-comment"),
    path("comment-edit/<int:id>/", views.EditComment.as_view(), name="edit-comment"),
    
    path("vote/<str:model>/<int:id>/", views.GenericVote.as_view(), name="generic-vote"), # str:model can be "topic" or "comment" gets the model to vote on and pass it to the view
    path("follow/<str:model>/<int:id>/", views.GenericFollow.as_view(), name="generic-follow"), # str:model can be "topic" or "comment" gets the model to follow and pass it to the view

    path("search/", views.SearchView.as_view(), name="search"),

    path("notifications/latest/", views.LatestNotificationsView.as_view(), name="latest-notifications"),
    path("notifications/mark-read/<int:id>/", views.MarkNotificationsAsReadView.as_view(), name="mark-notification-read"),

    path("news/", views.NewsView.as_view(), name="news"),  # News page

    path("about/", views.AboutView.as_view(), name="about"),
]
