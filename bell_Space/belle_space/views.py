from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.http import JsonResponse
from .forms import AppointmentForm
from django.contrib import messages
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
        
    
class RegisterFormView(View):
    def get(self, request):
        return render(request, "login.html")



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
            appointment.user = request.user  # Assuming user is logged in
            appointment.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('appointment_success')
        
        # If form is not valid, re-render the form with errors
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
    return render(request, "appointment_success.html")

