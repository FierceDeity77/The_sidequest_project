from django.contrib.contenttypes.models import ContentType
from content.models.notification_model import Notification

def create_notification(recipient, actor, verb, obj=None):
     if actor == recipient:
        return  # Don't notify self-actions
     # Create the notification when this function is called
     Notification.objects.create(
        actor=actor,
        recipient=recipient,
        verb=verb,
        content_type=ContentType.objects.get_for_model(obj) if obj else None,
        object_id=obj.id if obj else None,
     )