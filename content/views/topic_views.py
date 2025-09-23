from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Count
from django.contrib import messages
from content.models.community_model import Community
from content.models.topic_model import Topic
from content.forms import CommentForm, TopicForm
from django.contrib.auth.mixins import LoginRequiredMixin


class TopicDetail(View):
    def get(self, request, slug):
        community = get_object_or_404(Community, topics__slug=slug) # (reverse relation) ensure the topic belongs to a community
        topic = (Topic.objects
                    .annotate(
                        upvote_count=Count("upvotes", distinct=True),
                        downvote_count=Count("downvotes", distinct=True),
                    )
                    .get(slug=slug)
                )
        comment_list = topic.comments.all().order_by('-created_at')  # newest first
        comment_form = CommentForm()
        return render(request, "content/topic_detail.html", {"topic": topic,
                                                             "community": community, # to pass community data to topics detail so that the right panel can render the info
                                                             "comment_form": comment_form,
                                                             "comment_list": comment_list})
    

class CreateTopic(LoginRequiredMixin, View):
    def post(self, request, slug):
        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            topic = topic_form.save(commit=False)
            topic.community = Community.objects.get(slug=slug)
            topic.author = request.user
            topic.save()
            messages.success(request, "Topic created successfully!")
            return redirect("content:community-detail", slug=slug)
        return render(request, "content/community_detail.html", {"topic_form": topic_form})
    