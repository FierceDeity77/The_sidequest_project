from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Comments(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now_add=True)

    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="comment_upvotes", blank=True)
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="comment_downvotes", blank=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    # ---- Generic relation to ANY model ----
    content_type = models.ForeignKey(ContentType, null=True,on_delete=models.CASCADE)  # tells Django what model
    object_id = models.PositiveIntegerField(null=True)  # stores the ID of that object
    content_object = GenericForeignKey("content_type", "object_id")  # links to the object
    # use "content_object" related_name for reverse relation 

     # This allows a comment to be a reply to another comment, relationship to itself
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    class Meta:
        ordering = ['-created_at']  # to set the default ordering of comments by newest first