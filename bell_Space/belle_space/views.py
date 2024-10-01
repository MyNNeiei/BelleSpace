from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.http import JsonResponse
from .forms import AppointmentForm
from django.contrib import messages
from .forms import *
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
class IndexView(View):
    def get(self, request):
        user = User.objects.all()
        context = {"user" : user,}
        return render(request, "index.html", context)
    
# class AppointmentFormView(View):
#     def get(self, request):
#         form = AppointmentForm()
#         return render(request, "appointment_form.html", {"form": form})
#     def post(self, request):
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('appoint')
#         return render(request, "appointment_form.html", {"form": form})

    
class AppointmentView(View):
    def get(self, request):
        project = Appointment.objects.all()
        context = {"project" : project}
        return render(request, "project.html", context)
    
    def delete(self, request,dele):
        pro_id = Appointment.objects.get(id=dele)
        pro_id.delete()
        return JsonResponse({'status': 'ok'})
    
# class AppointmentDetailView(View):
#     def get(self, request, detail):
#         appointment = Appointment.objects.get(pk=detail)
#         form = AppointmentForm(instance=appointment)
#         # all_project = project_detail.staff.all()
#         adate = appointment.appointment_date.strftime("%Y-%m-%d")

#         context = { "form" : form,
#                     "appointment": appointment,
#                     "adate" : adate,}
#                     # "all_project" : all_project}
#         return render(request, "index.html", context)
    
#     def post(self, request, detail):
#         # for updating article instance set instance=article
#         appointment = Appointment.objects.get(pk=detail)
#         form = AppointmentForm(request.POST, instance= appointment)
#         # all_project = project_detail.staff.all()
#         adate = appointment.appointment_date.strftime("%Y-%m-%d")
#         context = { "form" : form,
#                     "appointment": appointment,
#                     "adate" : adate,}
#                     # "all_project" : all_project}
#         # save if valid                                       
#         if form.is_valid():                                                                      
#             form.save()                                                                          
#             return render(request, "index.html",context)

#         return render(request, "index.html", context)
class LoginFormView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "login/login_form.html" , {"form": form})
    def post(self, request):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('login_form.html')
        return render(request, "login/register_form.html", {"form": form})        
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login_form')

class RegisterFormView(View):
    def get(self, request):
        form = UserRegisterForm()
        formdetail = UserdetailRegisterForm()
        context = {
            "userform": form,
            "formdetail": formdetail
        }

        return render(request, "login/register_form.html" , context)
    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            UsersDetail.objects.create(
                user = user,
                phone_number = form.cleaned_data['phone_number'],
                birth_date = form.cleaned_data['birth_date'],
                gender = form.cleaned_data['gender']
            )
            return redirect('login_form.html')
        return render(request, "register_form.html", {"form": form})
