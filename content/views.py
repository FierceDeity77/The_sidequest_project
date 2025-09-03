from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import GameForm, TopicForm, CommentForm
from django.contrib import messages
from .models import Community, Game, Topic, Comments
from django.utils import timezone
import requests



class Home(View):
    def get(self, request):
        
        # headers = {
        #     "Authorization": ""
        # }

        # params = {
        #     "language.code": "en",
        #     "per_page": 3,
        #     "category.id": "medtop:20000548"
        # }

        # response = requests.get(api_endpoint, headers=headers, params=params)
        # data = response.json()

        # article = data["results"]
        article = [{
            "image": "images/final fantasy.png",
            "title": "Final Fantasy",
            "description": "RPG",
            "url": ""
        }, 
        {
            "image": "images/monster hunter.jpg",
            "title": "Monster Hunter",
            "description": "Action RPG",
            "url": ""
        },
        {
            "image": "images/resident evil.jpeg",
            "title": "Resident Evil",
            "description": "Survival Horror",
            "url": ""
        }]

        return render(request, "content/home.html", {"user": request.user, "article": article}) # request.user django built-in func to get current user

    def post(self, request):
        pass
    


class AddGame(LoginRequiredMixin, View):
    def get(self, request):
        game_form = GameForm()
        return render(request, "content/add_game.html", {"game_form": game_form})
    

    def post(self, request):
        game_form = GameForm(request.POST)
        if game_form.is_valid():
            game_data = game_form.save(commit=False) 
            game_data.author = request.user # gets the author id of the current user then saves it, assign the whole instance instead of just id
            game_data.content_type = "Game"
            game_data.save()

            messages.success(request, "Game Added!")
            return redirect("content:home")
        
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
        topics = community.topics.all().order_by('-created_at')  # newest first
        return render(request, "content/community_detail.html", {"community": community, 
                                                                 "topics": topics})


class CreateTopic(LoginRequiredMixin, View):
    def get(self, request, slug):
        topic_form = TopicForm()
        community = Community.objects.get(slug=slug) # to get the data of the current community
        return render(request, "content/create_topic.html", {"topic_form": topic_form, 
                                                             "slug": slug,
                                                             "community": community})

    def post(self, request, slug):
        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            topic = topic_form.save(commit=False)
            topic.community = Community.objects.get(slug=slug)
            topic.author = request.user
            topic.save()
            messages.success(request, "Topic created successfully!")
            return redirect("content:community_detail", slug=slug)
        return render(request, "content/create_topic.html", {"topic_form": topic_form})


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


class Discussions(View):
    def get(self, request):
        return render(request, "content/discussion.html")


    def post(self, request):
        pass


class Explore(View):
    def get(self, request):
        return render(request, "content/explore.html")


    def post(self, request):
        pass
