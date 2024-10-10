from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="home"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    # path("profile/edit_pass/", views.ChangePassword.as_view(), name="change_password"),
    path("register/", views.RegisterFormView.as_view(), name="register_form"),
    path("login/", views.LoginFormView.as_view(), name="login_form"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("appointment/", views.AppointmentView.as_view(), name="appointment"),
    
    path("appointment/<int:detail>", views.AppointmentDetailView.as_view(), name="appointment_detail"),
    path("appointment/<int:id>/delete/", views.AppointmentView.as_view(), name="appointment_delete"),
    path("appointment/<int:appointment_id>/<int:staff_id>/add/", views.AppointmentDetailView.as_view(), name="appointment_detail_add"),
    path("appointment/appointment_form/", views.AppointmentFormView.as_view(), name="appointment_form"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)