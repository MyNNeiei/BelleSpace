from django.urls import path
from . import views
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="home"),
    path("profile/", views.RegisterFormView.as_view(), name="profile"),
    path("register/", views.RegisterFormView.as_view(), name="register_form"),
    path("login/", views.LoginFormView.as_view(), name="login_form"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("appointment/", views.AppointmentView.as_view(), name="appointment"),
    path("appointment/<int:detail>", views.AppointmentDetailView.as_view(), name="appointment_detail"),
    path("appointment/<int:id>/delete/", views.AppointmentView.as_view(), name="appointment_delete"),
    path("appointment/<int:appointment_id>/<int:staff_id>/add/", views.AppointmentDetailView.as_view(), name="appointment_detail_add"), 
    path('appointment/appointment/', views.AppointmentFormView.as_view(), name='appointment_form'),
    path('appointment/appointment/load_services/', views.load_services, name='load_services'),  # Load services with the new function


]

