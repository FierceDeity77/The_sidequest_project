from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from content.models.community_model import Community
from django.db.models import Count
from content.forms import CommunityForm, SubCommunityForm, TopicForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import RoleRequiredMixin


class CommunityList(View):
    def get(self, request):
        # Annotate each community with the count of its members
        list_of_communities = (Community.objects.filter(is_main=True)
                                .annotate(member_count=Count("members"))).order_by("-member_count")
        
        list_of_subs = (Community.objects.filter(is_main=False)
                            .annotate(member_count=Count("members"))).order_by("-member_count")

        return render(request, "content/community.html", {"communities": list_of_communities,
                                                          "sub_communities": list_of_subs})
    

class CommunityDetail(View):
    def get(self, request, slug):
        community = get_object_or_404(
            Community.objects.annotate(member_count=Count("members")), slug=slug)
        # Get all sub-communities for the current community with most members first
        list_of_subs = (
                community.sub_communities.filter(is_main=False)
                .annotate(member_count=Count("members"))
                .order_by("-member_count")
        )

        community_form = CommunityForm(instance=community) # for modal edit community, instance in get prepopulates form fields with current model data.
        subcommunity_form = SubCommunityForm() # for modal create sub-community and returns a clear form
        topic_form = TopicForm()
        topics = community.topics.all() \
            .annotate(
                comment_count=Count("comments", distinct=True),
                upvote_count=Count("upvotes", distinct=True),
                downvote_count=Count("downvotes", distinct=True)
            ).order_by('-created_at')  # newest first, annotate calculates something per row and add it a extra fields to each topic object
        return render(request, "content/community_detail.html", 
                       {"community": community, 
                        "topics": topics,
                        "topic_form": topic_form,
                        "slug": slug, 
                        "community_form": community_form,
                        "subcommunity_form": subcommunity_form,
                        "list_of_subs": list_of_subs}) # pass id to check if creating sub-community
    

class AddSubCommunity(LoginRequiredMixin, View):
    def post(self, request, slug):
        parent_community = Community.objects.get(slug=slug)
        subcommunity_form = SubCommunityForm(request.POST, request.FILES) # for modal create sub-community
        if subcommunity_form.is_valid():
            sub_community = subcommunity_form.save(commit=False)
            sub_community.parent = parent_community
            sub_community.is_main = False
            sub_community.game = parent_community.game  # inherit the game from the parent community
            sub_community.content_type = "Sub-community"
            sub_community.created_by = request.user
            sub_community.save()
            # make the creator a moderator of the new sub-community
            sub_community.moderators.add(request.user)  
            messages.success(request, "Sub-community created successfully!")
            return redirect("content:community-detail", slug=slug)
        return render(request, "content/community_detail.html", {"subcommunity_form": subcommunity_form})


class EditCommunity(LoginRequiredMixin, RoleRequiredMixin, View):
    allowed_roles = ["admin", "moderator"]
    
    def get_object(self): # required for RoleRequiredMixin
        return Community.objects.get(slug=self.kwargs["slug"])
    

    def post(self, request, slug): # edit community detail goes to this post request
        community = self.get_object() # calls get_object func with rolereq mixin
        community_form = CommunityForm(request.POST, request.FILES, instance=community) # for modal edit community
        if community_form.is_valid():
            community = community_form.save(commit=False)
            community.save()
            community_form.save_m2m()
            return redirect("content:community-detail", slug=slug) 
        return render(request, "content/community_detail.html", {"community_form": community_form})
