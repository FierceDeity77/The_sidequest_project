from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from content.news import article  # import the article data from news.py

class NewsView(View):
    def get(self, request):
        return render(request, "content/news.html", {"article": article})