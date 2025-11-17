from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Count, FloatField, IntegerField, ExpressionWrapper
from content.forms import GameForm
from content.views.mixins import PaginationMixin
from content.game_api import search_igdb_games
from django.db.models.functions import NullIf, Coalesce
from content.models.game_model import Game # . only works if in the current folder this tells django to look into content app folder then models.py


class Games(View, PaginationMixin):
    def get(self, request): # renders the game list page and passes the form to add game form's modal
        game_form = GameForm()
        query_games = Game.objects.annotate(
            member_count=Count('members', distinct=True),
            upvote_count=Count('upvotes', distinct=True),
            downvote_count=Count('downvotes', distinct=True),
            # calculate net votes and output as IntegerField
            # net votes gets the difference between upvotes and downvotes
            net_votes=ExpressionWrapper(
                Count("upvotes", distinct=True) - Count("downvotes", distinct=True),
                output_field=IntegerField()
            ),
            # calculate approval percentage and output as FloatField
            # and sort by it
             # Approval percentage (0%–100%)
             # nullif to avoid division by zero and coalesce to set null percentages to 0.0
            percentage=Coalesce(
                ExpressionWrapper(
                    100.0 * Count('upvotes', distinct=True) /
                    NullIf(
                        Count('upvotes', distinct=True) + Count('downvotes', distinct=True),
                        0
                    ),
                    output_field=FloatField(),
                ),
                0.0
            )
        ).order_by('-percentage') # highest approval percentage first

        all_games = self.paginate_queryset(query_games, per_page=10, page_param="games_page")

        return render(request, "content/game_list.html", {"games": all_games, "game_form": game_form})
    

class GameDetail(View):
    def get(self, request, slug):
        game_info = Game.objects.annotate(
            member_count=Count("members", distinct=True),
            upvote_count=Count('upvotes', distinct=True),
            downvote_count=Count('downvotes', distinct=True),
            net_votes=ExpressionWrapper(
                Count("upvotes", distinct=True) - Count("downvotes", distinct=True),
                output_field=IntegerField()
            
        ) ).get(slug=slug)
        return render(request, "content/game_detail.html", {"game": game_info})
    

class AddGame(LoginRequiredMixin, View):
     def post(self, request):
        game_form = GameForm(request.POST, request.FILES) # add request.FILES to handle file uploads
        if game_form.is_valid():
            game_data = game_form.save(commit=False) 
            game_data.author = request.user # gets the current user instance
            game_data.content_type = "Game"
            game_data.save()
            game_form.save_m2m()  # for ManyToMany field

            # for AJAX
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string("content/includes/game_item.html", {"game": game_data})
                return JsonResponse({"success": True, "new_game_html": html})
            return redirect("content:game-list")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": game_form.errors})

        return render(request, "content/add_game_modal.html", {"game_form": game_form})