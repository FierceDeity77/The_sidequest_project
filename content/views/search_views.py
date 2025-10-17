from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from accounts.models import CustomUser
from content.views.mixins import PaginationMixin
from content.models.topic_model import Topic
from content.models.community_model import Community
from content.models.game_model import Game
from itertools import chain


class SearchView(View, PaginationMixin):
    def get(self, request):
        query = request.GET.get('q', '')

         # Filter each model
         # values makes querysets return the same columns
         # union requires same number of columns and compatible types
         # use Value to add a constant column to identify the type of each result
         # union slower and limited you get dictionaries instead of model instances
         # it's nice for sql merging but not for complex queries
         # if you need model instances consider using itertools.chain
         
        topics = Topic.objects.filter(title__icontains=query)
        communities = Community.objects.filter(name__icontains=query)
        games = Game.objects.filter(title__icontains=query)
        users = CustomUser.objects.filter(username__icontains=query)

        # Merge all results into one list
        search_results = list(chain(topics, communities, games, users))

        # Sort by created_at descending
        search_results.sort(key=lambda x: x.created_at, reverse=True)

        # Paginate results
        paginated_results = self.paginate_queryset(search_results, per_page=20, page_param="search_page")

        return render(request, "content/search_results.html", {"search_results": paginated_results, "query": query})