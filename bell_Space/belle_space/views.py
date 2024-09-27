from django.shortcuts import render
from django.views import View
from .models import *
# Create your views here.
class IndexView(View):
    def get(self, request):
        user = User.objects.all()
        context = {"user" : user,}
        return render(request, "index.html", context)