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
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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
        return render(request, "login/register_form.html" , {"form": form})
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            UsersDetail.objects.create(
                user=user,
                gender=form.cleaned_data['gender'],
                phone_number=form.cleaned_data['phone_number'],
                birth_date=form.cleaned_data['birth_date'],
                image_profile=form.cleaned_data.get('image_profile')
            )

            login(request, user)
            return redirect('login_form')
        # If forms are invalid, re-render the form with errors
        return render(request, 'index.html', {"form": form})
    
class ProfileView(View):
    def get(self, request):
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
    
# class AppointmentFormView(View):
#     def get(self, request):
#         form = AppointmentForm()
#         staff_list = Staff.objects.all()
#         categories = Categories.objects.all()
#         services = Service.objects.all().select_related('category')
        
#         # Group services by category
#         services_by_category = {}
#         for service in services:
#             if service.category.id not in services_by_category:
#                 services_by_category[service.category.id] = []
#             services_by_category[service.category.id].append(service)

#         context = {
#             "form": form,
#             "staff_list": staff_list,
#             "categories": categories,
#             "services_by_category": services_by_category,
#         }
#         return render(request, "appointment_form.html", context)

#     def post(self, request):
#         form = AppointmentForm(request.POST)

#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.user_id = request.user # Assuming user is logged in
#             appointment.save()

#             return redirect('appointment')



#     def appointment_success(request):
#         return render(request, "index.html")


    


class AppointmentDetailView(View):
    def get(self, request, detail):
        appointment_detail = Appointment.objects.get(pk=detail)
        form = AppointmentDetailForm(instance=appointment_detail)
        all_appointment = appointment_detail.staff_id.all()

        context = { "form" : form,
                    "appointment_detail":appointment_detail,
                    "all_appointment" : all_appointment}
        return render(request, "appointment_detail.html", context)
    
    def post(self, request, detail):
        # for updating article instance set instance=article
        appointment_detail = Appointment.objects.get(pk=detail)
        form = AppointmentDetailForm(request.POST, instance=appointment_detail)
        all_appointment = appointment_detail.staff_id.all()

        context = { "form" : form,
                    "appointment_detail": appointment_detail,
                    "all_appointment" : all_appointment}
                    
        # save if valid                                       
        if form.is_valid():                                                                      
            form.save()                                                                          
            return redirect('appointment')

        return render(request, "appointment_detail.html", context)
    
    def put(self, request, appointment_id, staff_id):
        appointment = Appointment.objects.get(id=appointment_id)
        staff = Staff.objects.get(id=staff_id)
        if staff not in appointment.staff_id.all():
            appointment.staff_id.add(staff)
            return redirect('appointment')
        return JsonResponse({'status': 'ok'})
    
    


class AppointmentView(View):
    def get(self, request):
        appointments = Appointment.objects.annotate(
            fullname=Concat(F('user_id__first_name'), Value(' '), F('user_id__last_name'))
        ).order_by('appointment_date')

        # Annotate services for each appointment
        for appointment in appointments:
            appointment.services = appointment.service.all()

        appointment_num = appointments.count()
        context = {
            "num": appointment_num,
            "appointments": appointments
        }
        return render(request, "appointment.html", context)
        

class AppointmentFormView(View):
    def get(self, request):
        form = AppointmentForm()
        return render(request, 'appointment_form.html', {"form": form})

    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user_id = request.user  # Assuming user is logged in
            appointment.save()

            # Saving the selected services
            form.save_m2m()  # This saves the many-to-many relationships
            return redirect('appointment')

        return render(request, 'appointment_form.html', {"form": form})



def load_services(request):
    category_id = request.GET.get("category")
    services = Service.objects.filter(category_id=category_id)
    return render(request, "service_options.html", {"services": services})

