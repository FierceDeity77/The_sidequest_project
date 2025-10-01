from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from django.contrib import messages
from content.models.topic_model import Topic
from content.models.comment_model import Comments
from content.forms import CommentForm


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
    
    
class DeleteComment(LoginRequiredMixin, View):
    def post(self, request, id):
        comment = get_object_or_404(Comments, id=id)

        # Only the author or a topic/community moderator can delete the comment
        if request.user != comment.author and request.user not in comment.content_object.community.moderators.all():
            messages.error(request, "You don't have permission to delete this comment.")
            return redirect("content:topic-detail", slug=comment.content_object.slug)

        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect("content:topic-detail", slug=comment.content_object.slug)
    
    
class EditComment(LoginRequiredMixin, View):
    def post(self, request, id):
        comment = get_object_or_404(Comments, id=id)

        # Only the author can edit the comment
        if request.user != comment.author:
            messages.error(request, "You don't have permission to edit this comment.")
            return redirect("content:topic-detail", slug=comment.content_object.slug)

        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, "Comment updated successfully!")
            return redirect("content:topic-detail", slug=comment.content_object.slug)
        
        return render(request, "content/edit_comment.html", {"comment_form": comment_form, "comment": comment})