from django.shortcuts import render
from django.views import View
from .models import *
# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, "index.html")
    
class RegisterFormView(View):
    def get(self, request):
        return render(request, "login.html")