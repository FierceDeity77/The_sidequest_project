from django.contrib.auth.mixins import LoginRequiredMixin
from content.models.notification_model import Notification
from django.views import View
from django.http import JsonResponse


class LatestNotificationsView(LoginRequiredMixin, View):
    def get(self, request):
        # query the latest 5 notifications for the logged-in user
        latest_notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:5]
        unread_count = Notification.objects.filter(
                        recipient=request.user, is_read=False
                        ).count()
        notifications_data = []

        for n in latest_notifications:
            message = ""
            if n.verb == 'upvote':
                message = f" {n.actor.username} upvoted your post"
            elif n.verb == 'comment':
                message = f"💬 {n.actor.username} commented on your post"
            elif n.verb == 'reply':
                message = f"↩️ {n.actor.username} replied to your comment"
            elif n.verb == 'message':
                message = f"✉️ {n.actor.username} sent you a message"
            elif n.verb == 'topic':
                # content_object is the model instance bcause of GenericForeignKey in Notification model
                message = f"📢 {n.actor.username} created a new topic in {n.content_object.name}"
            # append the notification data to the list
            notifications_data.append({
                    'message': message,
                    'created_at': n.created_at.strftime('%b %d, %Y %H:%M'),
                    'is_read': n.is_read,
                    'id': n.id,
                })
            # pass the notifications data as json response to the frontend javascript fetch call
        return JsonResponse({'notifications': notifications_data,
                             'unread_count': unread_count})
    
    
class MarkNotificationsAsReadView(LoginRequiredMixin, View):
    def post(self, request, id):
        if request.method == 'POST' and request.user.is_authenticated:
            try:
                notif = Notification.objects.get(pk=id, recipient=request.user)
                notif.is_read = True
                notif.save()
                return JsonResponse({'success': True})
            except Notification.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Notification not found'})
        return JsonResponse({'success': False, 'error': 'Invalid request'})