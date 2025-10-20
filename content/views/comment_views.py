from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from django.contrib import messages
from content.models.topic_model import Topic
from content.models.comment_model import Comments
from django.http import JsonResponse
from django.template.loader import render_to_string
from content.forms import CommentForm
from content.views.notification_utils_views import create_notification


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
            if parent_id: # check the parent_id if it has a value if yes then it's a reply
                parent_comment = get_object_or_404(Comments, id=parent_id) # use 404 if the object must exist
                comment_data['parent'] = parent_comment # set parent comment and updates inside the dict
                # create notification for reply
                create_notification(actor=request.user, recipient=parent_comment.author, verb='reply', obj=parent_comment)
                
            new_comment = Comments.objects.create(**comment_data) # set the dict as kwargs
            
            # Render the new comment HTML using your template tag
            # If AJAX request, return JSON instead of redirect
            # render_to_string to render the comment template to a string
            # and pass it back in the JSON response
            # because with AJAX we don't want to reload the whole page
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                comment_html = render_to_string(
                    "content/comments/comment.html",
                    {"comment": new_comment, "topic": topic, "request": request},
                    request=request,
                )
                return JsonResponse({
                    "success": True,
                    "comment_html": comment_html,
                    "parent_id": parent_id,
                })

            messages.success(request, "Reply added successfully!")
            return redirect("content:topic-detail", slug=slug)

        # Handle invalid form
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": comment_form.errors})
        return redirect("content:topic-detail", slug=slug)
             
    
class DeleteComment(LoginRequiredMixin, View):
    def post(self, request, id):
        comment = get_object_or_404(Comments, id=id)

        # Only the author, admin or a topic/community moderator can delete the comment
        if request.user != comment.author and request.user not in comment.content_object.community.moderators.all() and not request.user.is_staff:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"error": "You don't have permission to delete this comment."}, status=403)
            
            messages.error(request, "You don't have permission to delete this comment.")
            return redirect("content:topic-detail", slug=comment.content_object.slug)

        comment.delete()

         # AJAX response
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True, "message": "Comment deleted successfully!", "comment_id": id})
        
        messages.success(request, "Comment deleted successfully!")
        return redirect("content:topic-detail", slug=comment.content_object.slug)
    
    
class EditComment(LoginRequiredMixin, View):
    def post(self, request, id):
        comment = get_object_or_404(Comments, id=id)

        # Only the author and the admin can edit the comment
        if request.user != comment.author and not request.user.is_staff:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"error": "You don't have permission to edit this comment."}, status=403)
            messages.error(request, "You don't have permission to edit this comment.")
            return redirect("content:topic-detail", slug=comment.content_object.slug)

        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()

            # Handle AJAX request
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": True,
                    "comment_id": comment.id,
                    "new_text": comment.text
                })

            # Handle normal request (page reload)
            messages.success(request, "Comment updated successfully!")
            return redirect("content:topic-detail", slug=comment.content_object.slug)

        # Form errors
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"error": comment_form.errors}, status=400)

        return render(request, "content/edit_comment.html", {
            "comment_form": comment_form,
            "comment": comment
        })