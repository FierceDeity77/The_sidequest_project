from django.shortcuts import redirect, get_object_or_404
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