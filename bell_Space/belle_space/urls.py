from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="home"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    path("register/", views.RegisterFormView.as_view(), name="register_form"),
    path("login/", views.LoginFormView.as_view(), name="login_form"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("appointment/appointment_form/", views.AppointmentFormView.as_view(), name="appointment_form"),
    path("appointment/", views.AppointmentView.as_view(), name="appointment"),
    path("appointment/<int:detail>/", views.AppointmentAddStaffView.as_view(), name="appointment_addstaff"),
    path("appointment/<int:detail>/status/", views.AppointmentEditStatusView.as_view(), name="appointment_editstatus"),
    path("appointment/<int:id>/delete/", views.AppointmentView.as_view(), name="appointment_delete"),
    path('appointment/appointment_form/load_services/', views.load_services, name='load_services'),  


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


