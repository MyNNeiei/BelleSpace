from django.shortcuts import render, redirect
from django.views import View
from django.db.models.functions import Concat
from django.db.models import Value,F,Count
from .models import *
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
class IndexView(View):
    def get(self, request):
        user_in_customer_group = request.user.groups.filter(name='Customer').exists()
        user_in_manager_group = request.user.groups.filter(name='Manager').exists()
        user_in_staff_group = request.user.groups.filter(name='Staff').exists()
        context = {
            'user_in_customer_group': user_in_customer_group,
            'user_in_manager_group' : user_in_manager_group,
            'user_in_staff_group' : user_in_staff_group
            # other context variables
        }
        return render(request, "index.html", context)
    
        
class LoginFormView(View):
    def get(self, request):
        form = AuthenticationForm()

        return render(request, "login/login_form.html" , {"form": form})
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            user_groups = user.groups.all()
            for group in user_groups:
                get_group = group.name  
                
                # ผู้ใช้ตรงกับ group ไหน เด้งไปหน้านั้น
                if get_group == "Customer":
                    login(request, user)
                    return redirect('home')
                
                elif get_group == "Staff":
                    login(request, user)
                    return redirect('home')

                elif get_group == "Manager":
                    login(request, user)
                    return redirect('home')
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
            user = form.save()
            user.set_password(form.cleaned_data['password1'])
            user.save()
            UsersDetail.objects.create(
                user=user,
                gender=form.cleaned_data['gender'],
                phone_number=form.cleaned_data['phone_number'],
                birth_date=form.cleaned_data['birth_date'],
                image_profile=form.cleaned_data.get('image_profile')
            )
            customer_group = Group.objects.get(name='Customer')  # Replace with your group name
            user.groups.add(customer_group)
            login(request, user)
            return redirect('login_form')
        # If forms are invalid, re-render the form with errors
        print(form.errors)
        return render(request, 'login/register_form.html', {"form": form})

   
class ProfileView(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = '/login/'
    permission_required = ["belle_space.view_usersdetail"]
    def get(self, request):
        user_in_customer_group = request.user.groups.filter(name='Customer').exists()
        user_in_manager_group = request.user.groups.filter(name='Manager').exists()
        user_in_staff_group = request.user.groups.filter(name='Staff').exists()
        context = {
            'user_in_customer_group': user_in_customer_group,
            'user_in_manager_group' : user_in_manager_group,
            'user_in_staff_group' : user_in_staff_group
            # other context variables
        }
        return render(request, 'profile/profile.html' ,context)

class ProfileEditView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["belle_space.change_usersdetail"]
    def get(self, request):
        user = request.user
        userdetail = UsersDetail.objects.get(user=user)
        user_in_customer_group = request.user.groups.filter(name='Customer').exists()
        user_in_manager_group = request.user.groups.filter(name='Manager').exists()
        user_in_staff_group = request.user.groups.filter(name='Staff').exists()
        context = {
            'user_in_customer_group': user_in_customer_group,
            'user_in_manager_group' : user_in_manager_group,
            'user_in_staff_group' : user_in_staff_group
            # other context variables
        }
        form = EditProfileForm(instance=user,initial={
            'birth_date': userdetail.birth_date,
            'phone_number': userdetail.phone_number,
            'gender': userdetail.gender,
            'image_profile' : userdetail.image_profile})
        return render(request, 'profile/edit_profile.html', {'form': form,
                                                             'context': context})

    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        print(form.errors)
        if form.is_valid():
            userdetail = UsersDetail.objects.get(user=user)
            userdetail.phone_number = form.cleaned_data['phone_number']
            userdetail.gender = form.cleaned_data['gender']
            userdetail.birth_date = form.cleaned_data['birth_date']
            new_images = request.FILES.get('image_profile')
            userdetail.image_profile = new_images
            userdetail.save()
            return redirect('profile')
        return render(request, 'profile/profile.html', {'form': form})
class ChangePassword(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["belle_space.change_usersdetail"]
    def post(self, request):
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for keeping the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
        
        form = ChangePasswordForm(user=request.user)
        return render(request, 'change_password.html', {'form': form})
class AppointmentView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/login/'
    permission_required = ["belle_space.view_appointment"]
    def get(self, request):
        appointments = Appointment.objects.annotate(
            fullname=Concat(F('user__first_name'), Value(' '), F('user__last_name'))
        ).order_by('appointment_date')
        appoint_staff = Appointment.objects.filter(staff = request.user.id)
        appoint_customer = Appointment.objects.filter(user = request.user.id)
        user_in_customer_group = request.user.groups.filter(name='Customer').exists()
        user_in_manager_group = request.user.groups.filter(name='Manager').exists()
        user_in_staff_group = request.user.groups.filter(name='Staff').exists()
        # Annotate services for each appointment
        if user_in_customer_group:
            # Show customer's own appointments
            appointments_to_display = appoint_customer
        elif user_in_manager_group:
            # Manager sees all appointments
            appointments_to_display = appointments
        elif user_in_staff_group:
            # Staff sees only their appointments
            appointments_to_display = appoint_staff
        else:
            # If not in any of the groups, display no appointments
            appointments_to_display = []
        for appointment in appointments:
            appointment.services = appointment.service.all()

        appointment_num = appointments.count()
        context = {
            "num": appointment_num,
            "appointments": appointments_to_display,
            'user_in_customer_group': user_in_customer_group,
            'user_in_manager_group' : user_in_manager_group,
            'user_in_staff_group' : user_in_staff_group,
            'appoint_staff' : appoint_staff,
            'appoint_customer' : appoint_customer
        }

        
        return render(request, "appointment.html", context)
    
    def delete(self, request, id):
        appointment = Appointment.objects.get(pk=id)
        time_remaining = appointment.appointment_date - timezone.now()
        if time_remaining.total_seconds() < 3600:  # น้อยกว่า 1 ชั่วโมง (3600 วินาที)
            return JsonResponse({'status': 'error', 'message': 'ไม่สามารถลบการนัดหมายได้ภายใน 1 ชั่วโมงก่อนเวลานัดหมาย'})
        appointment.staff.clear()  # Clear the many-to-many relationships
        appointment.delete()
        return JsonResponse({'status': 'ok'})
# @login_required
class AppointmentAddStaffView(View):
    def get(self, request, detail):
        appointment_detail = Appointment.objects.get(pk=detail)
        form = AppointmentAddStaffForm(instance=appointment_detail)
        all_appointment = appointment_detail.staff.all()
        user_in_customer_group = request.user.groups.filter(name='Customer').exists()
        user_in_manager_group = request.user.groups.filter(name='Manager').exists()
        user_in_staff_group = request.user.groups.filter(name='Staff').exists()
        context = { "form" : form,
                   'user_in_customer_group': user_in_customer_group,
            'user_in_manager_group' : user_in_manager_group,
            'user_in_staff_group' : user_in_staff_group}
        return render(request, "appointment_addstaff.html", context)
    
    def post(self, request, detail):
        # for updating article instance set instance=article
        appointment_detail = Appointment.objects.get(pk=detail)
        form = AppointmentAddStaffForm(request.POST, instance=appointment_detail)
        all_appointment = appointment_detail.staff.all()
        user_in_customer_group = request.user.groups.filter(name='Customer').exists()
        user_in_manager_group = request.user.groups.filter(name='Manager').exists()
        user_in_staff_group = request.user.groups.filter(name='Staff').exists()
        context = { "form" : form,
                   'user_in_customer_group': user_in_customer_group,
            'user_in_manager_group' : user_in_manager_group,
            'user_in_staff_group' : user_in_staff_group}                                             
        if form.is_valid():                                                                      
            form.save()                                                                          
            return redirect('appointment')

        return render(request, "appointment_addstaff.html", context)
    
    def put(self, request, appointment_id, staff_id):
        appointment = Appointment.objects.get(id=appointment_id)
        staff = Staff.objects.get(id=staff_id)
        if staff not in appointment.staff_id.all():
            appointment.staff_id.add(staff)
            return redirect('appointment')
        return JsonResponse({'status': 'ok'})
    
    
class AppointmentEditStatusView(View):
    def get(self, request, detail):
        appointment_detail = Appointment.objects.get(pk=detail)
        form = AppointmentEditStatusForm(instance=appointment_detail)

        context = {
            "form": form,
        }
        return render(request, "appointment_editstatus.html", context)

    def post(self, request, detail):
        appointment_detail = Appointment.objects.get(pk=detail)
        form = AppointmentEditStatusForm(request.POST, instance=appointment_detail)

        if form.is_valid():
            form.save()
            return redirect('appointment')

        context = {
            "form": form,
        }
        return render(request, "appointment_editstatus.html", context)



class AppointmentFormView(LoginRequiredMixin, PermissionRequiredMixin , View):
    login_url = '/login/'
    permission_required = ["belle_space.add_appointment"]
    def get(self, request):
        form = AppointmentForm()
        user_in_customer_group = request.user.groups.filter(name='Customer').exists()
        user_in_manager_group = request.user.groups.filter(name='Manager').exists()
        user_in_staff_group = request.user.groups.filter(name='Staff').exists()
        context = {
            'user_in_customer_group': user_in_customer_group,
            'user_in_manager_group' : user_in_manager_group,
            'user_in_staff_group' : user_in_staff_group
            # other context variables
        }
        return render(request, 'appointment_form.html', {"form": form,
                                                         'context':context})

    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  # Assuming user is logged in
            appointment_date = appointment.appointment_date.date()  # Get just the date part
            category = appointment.category  # Assuming there's a 'category' field in the Appointment model

            # Check if the user already has an appointment with the same category on the same day
            existing_appointment = Appointment.objects.filter(
                user=request.user,
                appointment_date__date=appointment_date,
                category=category  # Assuming 'category' is a field in your Appointment model
            ).exists()

            if existing_appointment:
                messages.error(request, "คุณสามารถจองบริการได้เพียง 1 ประเภทต่อวัน")
                return render(request, 'appointment_form.html', {"form": form})
            appointment.save()

            # Saving the selected services
            form.save_m2m()  # This saves the many-to-many relationships
            return redirect('appointment')

        return render(request, 'appointment_form.html', {"form": form})



def load_services(request):
    category_id = request.GET.get("category")
    services = Service.objects.filter(category_id=category_id)
    return render(request, "service_options.html", {"services": services})

