from datetime import date,datetime
from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, DateInput
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Appointment, Service
from django.utils import timezone

class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        ]
    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get("birth_date")
        birth_now = datetime.now().date()
        if birth_date > birth_now:
            raise ValidationError(
                    "birth_date ว่าจะต้องไม่เป็นวันในอนาคต"
            )
        return cleaned_data

# class UserDetailLoginForm(ModelForm):
#     class Meta:
#         model = UsersDetail
#         fields = [
#             "birth_date",
#             "phone_number"
#         ]
#         widgets = {
#             "birth_date" : DateInput(attrs={"type": "date"}),
#             }
#     def clean(self):
#         cleaned_data = super().clean()
#         birth_date = cleaned_data.get("hire_date")
#         birth_now = datetime.now().date()
#         if birth_date > birth_now:
#             raise ValidationError(
#                     "birth_date ว่าจะต้องไม่เป็นวันในอนาคต"
#             )
#         return cleaned_data

# อันนี้เด็ด
class AppointmentForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta:
        model = Appointment
        fields = ['staff', 'services', 'appointment_date']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        app_date = cleaned_data.get('appointment_date')
        now = timezone.now()

        if app_date and app_date < now:
            raise ValidationError("จองย้อนไม่ได้จ้า")
        
        return cleaned_data
