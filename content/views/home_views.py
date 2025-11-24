from django.views import View
from django.shortcuts import render
from django.db.models import Count
from content.models.topic_model import Topic
from django.views.generic import TemplateView


class Home(View):
    def get(self, request):    
        if request.user.is_authenticated:
            topics = (
                    Topic.objects.filter(community__members=request.user) # filter topics based on communities the user is a member of
                    .annotate(
                        upvote_count=Count("upvotes", distinct=True),
                        downvote_count=Count("downvotes", distinct=True),
                        comment_count=Count("comments", distinct=True),
                    )
                    .order_by("-created_at")
                    )
        else:
            topics = (
                    Topic.objects.all()
                    .annotate(
                        upvote_count=Count("upvotes", distinct=True),
                        downvote_count=Count("downvotes", distinct=True),
                        comment_count=Count("comments", distinct=True),
                    )
                    .order_by("-created_at")
                    )
        
        return render(request, "content/home.html", {"user": request.user,
                                                      "topics": topics,})
    
    
class AboutView(TemplateView):
    template_name = "content/about.html"