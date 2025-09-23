from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Count
from content.forms import GameForm
from content.models.game_model import Game # . only works if in the current folder this tells django to look into content app folder then models.py


class Games(View):
    def get(self, request): # renders the game list page and passes the form to add game form's modal
        game_form = GameForm()
        all_games = Game.objects.annotate(member_count=Count('members', distinct=True)
                                          ).order_by('-created_at')  # newest first
        return render(request, "content/game_list.html", {"games": all_games, "game_form": game_form})
    

class GameDetail(View):
    def get(self, request, slug):
        game_info = get_object_or_404(
            Game.objects.annotate(
                member_count=Count("members", distinct=True),), slug=slug)
        return render(request, "content/game_detail.html", {"game": game_info})
    

class AddGame(LoginRequiredMixin, View):
     def post(self, request):
        game_form = GameForm(request.POST, request.FILES) # add request.FILES to handle file uploads
        if game_form.is_valid():
            game_data = game_form.save(commit=False) 
            game_data.author = request.user # gets the author id of the current user then saves it, assign the whole instance instead of just id
            game_data.content_type = "Game"
            game_data.save()
            game_form.save_m2m()  # <-- VERY IMPORTANT for ManyToMany fields!

            # for AJAX
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                html = render_to_string("content/includes/game_item.html", {"game": game_data})
                return JsonResponse({"success": True, "new_game_html": html})
            return redirect("content:game-list")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": game_form.errors})

        return render(request, "content/add_game_modal.html", {"game_form": game_form})