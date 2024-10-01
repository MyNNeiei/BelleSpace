from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.http import JsonResponse
from .forms import *
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, "index.html")
    
class AppointmentFormView(View):
    def get(self, request):
        form = AppointmentForm()
        return render(request, "appointment_form.html", {"form": form})
    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appoint')
        return render(request, "appointment_form.html", {"form": form})
    

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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')# Redirect to home after successful login
        print(form.errors)
        return render(request, "login/login_form.html", {"form": form})        
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')

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
        userform = UserRegisterForm(request.POST)
        userdetailform = UserdetailRegisterForm(request.POST)
        if userform.is_valid() and userdetailform.is_valid():
            # มัน return เป็น user ogject
            user = userform.save()
            userdetil = UsersDetail.objects.create(user_id=user,
                                                    gender=userdetailform.cleaned_data['gender'],
                                                   phone_number=userdetailform.cleaned_data['phone_number'],
                                                   birth_date=userdetailform.cleaned_data['birth_date']
                                                  )
            # group customer
            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            user.save()
            login(request,user)
            return redirect('home')
        context = {"userform": userform, "userdetailform": userdetailform}
        return render(request, 'login/register_form.html', context)
    
class ProfileView(View):
    def get(self, request):
        return render(request, "index.html")