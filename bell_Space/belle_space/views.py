from django.shortcuts import render, redirect
from django.views import View
from django.db.models.functions import Concat
from django.db.models import Value,F,Count
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from .forms import *
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, "index.html")
    
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
    
class AppointmentFormView(View):
    def get(self, request):
        form = AppointmentForm()
        staff_list = Staff.objects.all()
        categories = Categories.objects.all()
        services = Service.objects.all().select_related('category')
        
        # Group services by category
        services_by_category = {}
        for service in services:
            if service.category.id not in services_by_category:
                services_by_category[service.category.id] = []
            services_by_category[service.category.id].append(service)

        context = {
            "form": form,
            "staff_list": staff_list,
            "categories": categories,
            "services_by_category": services_by_category,
        }
        return render(request, "appointment_form.html", context)

    def post(self, request):
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)

            # appointment.user = request.user # Assuming user is logged in
            appointment.user = 2 
            appointment.save()
            return redirect('appointment')

        staff_list = Staff.objects.all()
        categories = Categories.objects.all()
        services = Service.objects.all().select_related('category')
        services_by_category = {}
        for service in services:
            if service.category.id not in services_by_category:
                services_by_category[service.category.id] = []
            services_by_category[service.category.id].append(service)

        context = {
            "form": form,
            "staff_list": staff_list,
            "categories": categories,
            "services_by_category": services_by_category,
        }
        return render(request, "appointment_form.html", context)

    def appointment_success(request):
        return render(request, "index.html")

# class AppointmentView(View):
#     def get(self, request):
#         user_fullname = User.objects.annotate(fullname = Concat(F('first_name'),Value(' '),F('last_name')))
#         appoint_num = user_fullname.count()
#         context = {"num" : appoint_num,
#                     "fullname" : user_fullname}
#         return render(request, "appointment.html", context)
    
class AppointmentView(View):
    def get(self, request):
        appointments = Appointment.objects.annotate(
            fullname=Concat(F('user_id__first_name'), Value(' '), F('user_id__last_name'))
        ).order_by('-appointment_date')

        # Annotate services for each appointment
        for appointment in appointments:
            appointment.services = Service.objects.filter(category=appointment.category)

        appointment_num = appointments.count()
        context = {
            "num": appointment_num,
            "appointments": appointments
        }
        return render(request, "appointment.html", context)
