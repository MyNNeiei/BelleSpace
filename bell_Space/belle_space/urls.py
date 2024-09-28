from django.urls import path
from . import views
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="home"),
    path("appointment/", views.AppointmentView.as_view(), name="appointment"),
    path("appointment/appointment_form/", views.AppointmentFormView.as_view(), name="appointment_form"),
]