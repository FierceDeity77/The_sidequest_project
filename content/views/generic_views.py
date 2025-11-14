from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator # require login to cbv functions
from django.apps import apps
from content.views.notification_utils_views import create_notification


class GenericFollow(View): # reusable follow view for both communities and games to keep DRY
    @method_decorator(login_required(login_url='login'))
    def post(self, request, model, id):
        # Dynamically get model: "community" -> Community, "game" -> Game
        # this makes the follow view reusable for both communities and games

        # gets the model class from the string name and capitalize to match the class name
        Model = apps.get_model("content", model.capitalize())
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
        # this makes the vote view reusable for both topics, comments and games
        Model = apps.get_model("content", model.capitalize()) 
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

                # calls the create_notification function to notify the author of the upvote
                # if conditions to filter which model the upvote belongs to
                if Model.__name__ == "Topic":
                # obj=obj passes the model instance to the function call
                    create_notification(actor=request.user, recipient=obj.author, 
                                        url=reverse('content:topic-detail', args=[obj.slug]), 
                                        verb='upvote_topic', obj=obj)
                
                elif Model.__name__ == "Comments":
                     create_notification(actor=request.user, recipient=obj.author, 
                                        url=reverse('content:topic-detail', args=[obj.id]), 
                                        verb='upvote_comment', obj=obj)

                # If user upvotes, remove downvote if exists
                obj.downvotes.remove(request.user)
                obj.author.karma += 1 # Increases user's xp/karma for upvote
                obj.author.save()

                # if game model then author does not get karma
                if Model.__name__ in ["Game"]:
                    obj.author.karma += 0
                    obj.author.save()
                 
        elif action == "downvote":
            if already_downvoted:
                obj.downvotes.remove(request.user)
            else:
                obj.downvotes.add(request.user)
                obj.upvotes.remove(request.user)

                # reduces karma if models from topic or comments
                if Model.__name__ in ["Topic", "Comments"]:
                    obj.author.karma -= 1
                    obj.author.save()
    
        return JsonResponse({
            "upvotes": obj.upvotes.count(),
            "downvotes": obj.downvotes.count(),
        })
    
