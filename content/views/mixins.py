from django.http import HttpResponseForbidden

class RoleRequiredMixin:
    """
    Restricts access to users with specific global roles 
    OR who are moderators of the given community.
    """
    allowed_roles = []
    community_field = "community"  # default attr to check moderators against

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object() # get_object could be a community, topic, etc.
         # Get the community instance to check moderators against
        community = getattr(obj, self.community_field, obj)

       # If role is allowed, pass
        if request.user.role in self.allowed_roles:
            return super().dispatch(request, *args, **kwargs)

        # If user is a moderator of this community, also pass
        if request.user in community.moderators.all():
            return super().dispatch(request, *args, **kwargs)

        # Otherwise block
        return HttpResponseForbidden("You don’t have permission to perform this action.")