from django.shortcuts import render
from django.views import View

class Guides(View):
    def get(self, request):
        return render(request, "guides/guides.html")


    def post(self, request):
        pass