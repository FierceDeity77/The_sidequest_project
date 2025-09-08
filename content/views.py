from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import GameForm, TopicForm, CommentForm, CommunityForm
from django.contrib import messages
from .models import Community, Game, Topic, Comments
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # can require login to cbv functions
from .news import article  # import the article data from news.py



class Home(View):
    def get(self, request):    
        return render(request, "content/home.html", {"user": request.user, "article": article}) # request.user django built-in func to get current user

    def post(self, request):
        pass


class Games(View):
    def get(self, request): # renders the game list page and passes the form to add game form's modal
        game_form = GameForm()
        all_games = Game.objects.all().order_by('-created_at')  # newest first
        return render(request, "content/game_list.html", {"games": all_games, "game_form": game_form})


class GameDetail(View):
    def get(self, request):
        return render(request, "content/game_detail.html")


    def post(self, request):
        pass
    


class AddGame(LoginRequiredMixin, View):
     def post(self, request):
        game_form = GameForm(request.POST, request.FILES) # add request.FILES to handle file uploads
        if game_form.is_valid():
            game_data = game_form.save(commit=False) 
            game_data.author = request.user # gets the author id of the current user then saves it, assign the whole instance instead of just id
            game_data.content_type = "Game"
            game_data.save()

            # for AJAX
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string("content/includes/game_item.html", {"game": game_data})
                return JsonResponse({"success": True, "new_game_html": html})
            return redirect("content:game-list")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": game_form.errors})

        return render(request, "content/add_game.html", {"game_form": game_form})


class CommunityList(View):
    def get(self, request):
        list_of_communities = Community.objects.filter(is_main=True)
        list_of_subs = Community.objects.filter(is_main=False)
        return render(request, "content/community.html", {"communities": list_of_communities, 
                                                          "sub_communities": list_of_subs})


class CommunityDetail(View):
    def get(self, request, slug):
        community = Community.objects.get(slug=slug)
        community_form = CommunityForm(instance=community) # for modal edit community, instance in get prepopulates form fields with current model data.
        topic_form = TopicForm()
        topics = community.topics.all().order_by('-created_at')  # newest first
        return render(request, "content/community_detail.html", {"community": community, 
                                                                 "topics": topics,
                                                                 "topic_form": topic_form,
                                                                 "slug": slug, 
                                                                 "community_form": community_form})
    
    @method_decorator(login_required(login_url='login')) # method decorator adapts decorators like login required to work with cbv's
    def post(self, request, slug): # edit community detail goes to this post request
        community = Community.objects.get(slug=slug) # instance in post ensures you edit the same object instead of creating a new one
        community_form = CommunityForm(request.POST, request.FILES, instance=community) # for modal edit community
        if community_form.is_valid():
            community_form.save()
            return redirect("content:community-detail", slug=slug) 
        return render(request, "content/community_detail.html", {"community_form": community_form})


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


class TopicDetail(View):
    def get(self, request, slug):
        topic = Topic.objects.get(slug=slug)
        comment_list = topic.comments.all().order_by('-created_at')  # newest first
        comment_form = CommentForm()
        return render(request, "content/topic_detail.html", {"topic": topic, 
                                                             "comment_form": comment_form,
                                                             "comment_list": comment_list})

    
class AddComment(LoginRequiredMixin, View):
    def post(self, request, slug, parent_id=None): # set to None by default means it is a top-level comment
        topic = get_object_or_404(Topic, slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_data = {
                "text": comment_form.cleaned_data['text'],
                "content_object": topic,
                "created_at": timezone.now(),
                "parent": parent_id,
                "author": request.user,
            }
            if parent_id: # check if it has parent then if yes then it's a reply
                parent_comment = get_object_or_404(Comments, id=parent_id) # use this if the object must exist
                comment_data['parent'] = parent_comment # set parent comment and updates inside the dict
                Comments.objects.create(**comment_data) # set the dict as kwargs

            else: # no parent means it's a top-level comment
                Comments.objects.create(**comment_data)

            messages.success(request, "Reply added successfully!")
        return redirect("content:topic-detail", slug=slug)
    


class CreateSubCommunity(LoginRequiredMixin, View):
    def get(self, request, slug):
        game_form = GameForm()
        return render(request, "content/add_game.html", {"game_form": game_form})
    







class Reviews(View):
    def get(self, request):
        return render(request, "content/reviews.html")


    def post(self, request):
        pass


class Guides(View):
    def get(self, request):
        return render(request, "content/guides.html")


    def post(self, request):
        pass






