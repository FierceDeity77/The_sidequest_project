from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Count
from django.contrib import messages
from content.models.community_model import Community
from content.models.topic_model import Topic
from content.forms import CommentForm, TopicForm, CommunityForm, SubCommunityForm
from django.contrib.auth.mixins import LoginRequiredMixin
from content.views.notification_utils_views import create_notification


class TopicDetail(View):
    def get(self, request, slug):
         # (reverse relation) ensure the topic belongs to a community.
        community = get_object_or_404(
            Community.objects.annotate(member_count=Count("members")), topics__slug=slug)
        
        # Get all sub-communities for the current community with most members first
        list_of_subs = (
                community.sub_communities.filter(is_main=False)
                .annotate(member_count=Count("members"))
                .order_by("-member_count")
        )

        topic = (Topic.objects
                    .annotate(
                        upvote_count=Count("upvotes", distinct=True),
                        downvote_count=Count("downvotes", distinct=True),
                    )
                    .get(slug=slug)
                )
       
        # filter to get only top-level comments (parent is null) and order by newest first
        comment_list = topic.comments.filter(parent__isnull=True).order_by('-created_at')

        community_form = CommunityForm(instance=community) # for modal edit community, instance in get prepopulates form fields with current model data.
        subcommunity_form = SubCommunityForm() # for modal create sub-community and returns a clear form
        comment_form = CommentForm()
        topic_form = TopicForm(instance=topic)  # pass form with existing topic data for editing

        return render(request, "content/topic_detail.html", 
                       {"topic": topic,
                        "community": community, # to pass community data to topics detail so that the right panel can render the info
                        "comment_form": comment_form,
                        "comment_list": comment_list,
                        "topic_form": topic_form,
                        "community_form": community_form,
                        "subcommunity_form": subcommunity_form,
                        "list_of_subs": list_of_subs})


class AddTopic(LoginRequiredMixin, View):
    def post(self, request, slug):
        topic_form = TopicForm(request.POST)
        current_community = get_object_or_404(Community, slug=slug)
        if topic_form.is_valid():
            topic = topic_form.save(commit=False)
            topic.community = current_community
            topic.content_type = "Topic"
            topic.author = request.user
            topic.save()
            
            # create_notification(actor=request.user, recipient=current_community.created_by, 
            #                     verb='topic', obj=current_community)
            
            messages.success(request, "Topic created successfully!")
            return redirect("content:community-detail", slug=slug)
        return render(request, "content/community_detail.html", {"topic_form": topic_form})
    

class EditTopic(LoginRequiredMixin, View):
    def post(self, request, slug):
        topic = get_object_or_404(Topic, slug=slug)
        
        # Only the author can edit the topic
        if request.user != topic.author and not request.user.is_staff:
            messages.error(request, "You don't have permission to edit this topic.")
            return redirect("content:topic-detail", slug=slug)
        
        topic_form = TopicForm(request.POST, instance=topic)
        if topic_form.is_valid():
            topic_form.save()
            messages.success(request, "Topic updated successfully!")
            return redirect("content:topic-detail", slug=slug)
        return render(request, "content/edit_topic.html", {"topic_form": topic_form, "topic": topic})
    

class DeleteTopic(LoginRequiredMixin, View):
    def post(self, request, slug):
        topic = get_object_or_404(Topic, slug=slug)
        
            # Only the author, admin or a community moderator can delete the topic
            # checks if both conditions are false then no permission
        if request.user != topic.author and request.user not in topic.community.moderators.all() and not request.user.is_staff:
            messages.error(request, "You don't have permission to delete this topic.")
            return redirect("content:topic-detail", slug=slug)
        
        community_slug = topic.community.slug  # store community slug before deleting the topic
        topic.delete()
        messages.success(request, "Topic deleted successfully!")
        return redirect("content:community-detail", slug=community_slug)