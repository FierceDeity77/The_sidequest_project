from django.shortcuts import get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # can require login to cbv functions
from django.apps import apps


class GenericFollow(View): # reusable follow view for both communities and games to keep DRY
    @method_decorator(login_required(login_url='login'))
    def post(self, request, model, id):
        # Dynamically get model: "community" -> Community, "game" -> Game
        # this makes the follow view reusable for both communities and games
        Model = apps.get_model("content", model.capitalize()) # gets the model class from the string name and capitalize the first letter to match the class name
        obj = get_object_or_404(Model, id=id)

        if request.user in obj.members.all():
            obj.members.remove(request.user)
            is_following = False
        else:
            obj.members.add(request.user)
            is_following = True

        return JsonResponse({
            "is_following": is_following,
            "member_count": obj.members.count(),
        })
    

class GenericVote(View): # reusable vote view for both topics and comments to keep DRY
    @method_decorator(login_required(login_url='login'))
    def post(self, request, model, id):
        # Dynamically get model: "topic" -> Topic, "comment" -> Comments
        # this makes the vote view reusable for both topics and comments
        Model = apps.get_model("content", model.capitalize()) # gets the model class from the string name and capitalize the first letter to match the class name
        obj = get_object_or_404(Model, id=id)

        action = request.POST.get("action")

         # Check if the user already voted
        already_upvoted = obj.upvotes.filter(id=request.user.id).exists()
        already_downvoted = obj.downvotes.filter(id=request.user.id).exists()

        if action == "upvote":
            if already_upvoted:
                obj.upvotes.remove(request.user)
            else:
                obj.upvotes.add(request.user)
                # If user upvotes, remove downvote if exists
                obj.downvotes.remove(request.user)

                # checks to see if the model being voted on is Topic or Comments to adjust user's karma accordingly
                if Model.__name__ in ["Topic", "Comments"]:
                    obj.author.karma += 1
                    obj.author.save()
                 
        elif action == "downvote":
            if already_downvoted:
                obj.downvotes.remove(request.user)
            else:
                obj.downvotes.add(request.user)
                obj.upvotes.remove(request.user)

                # checks to see if the model being voted on is Topic or Comments to adjust user's karma accordingly
                if Model.__name__ in ["Topic", "Comments"]:
                    obj.author.karma -= 1
                    obj.author.save()
    
        return JsonResponse({
            "upvotes": obj.upvotes.count(),
            "downvotes": obj.downvotes.count(),
        })
    
