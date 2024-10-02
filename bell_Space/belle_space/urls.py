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
    path("appointment/appointment_form/", views.AppointmentFormView.as_view(), name="appointment_form"),
]