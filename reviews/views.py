from django.shortcuts import render
from django.views import View

class Reviews(View):
    def get(self, request):
        return render(request, "reviews/reviews.html")


    def post(self, request):
        pass
