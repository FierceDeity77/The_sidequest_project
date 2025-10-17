from django.http import HttpResponseForbidden
from django.core.paginator import Paginator


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
    

class PaginationMixin:
    def paginate_queryset(self, queryset, per_page=5, page_param="page"):
        paginator = Paginator(queryset, per_page)
        page_number = self.request.GET.get(page_param) # this is used to get different url paginations on the same page for example ?posts_page=2
        return paginator.get_page(page_number)
    """
    Generic paginator helper.
    - request: the current request object
    - queryset: any queryset to paginate
    - per_page: number of items per page (default 5)
    - page_param: the name of the GET parameter to use (default "page")
    """