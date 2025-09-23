from django.views import View
from django.shortcuts import render
from content.news import article  # import the article data from news.py


class Home(View):
    def get(self, request):    
        return render(request, "content/home.html", {"user": request.user, "article": article}) # request.user django built-in func to get current user