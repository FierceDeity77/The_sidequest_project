from django.db import models
from django.conf import settings 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('upvote_topic', 'Upvote_topic'),
        ('upvote_comment', 'Upvote_comment'),
        ('comment', 'Comment'),
        ('reply', 'Reply'),
        ('message', 'Message'),
        ('topic', 'Topic'),
    )

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    verb = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    url = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Generic relation to the object involved (e.g., Post, Comment)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.actor} {self.verb} {self.content_object} for {self.recipient}"
