from datetime import date,datetime
from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, DateInput
from django.core.exceptions import ValidationError
from .models import *

class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        ]
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

class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "first_name",
            "last_name",
            "service", 
            "staff",
            "appointment_date",
        ]
        model = User
        fields = [
            "first_name",
            "last_name",

        ]

        widgets = {
            "appointment_date" : DateInput(attrs={"type": "date"}),
            }
    
    def clean(self):   
        cleaned_data = super().clean()

        # service = cleaned_data.get("service")
        # staff = cleaned_data.get("staff")

        appointment_date = cleaned_data.get("appointment_date")
        appointment_date = datetime.now().date()
        if appointment_date < appointment_date:
            raise ValidationError(
                    "จองย้อนไม่ได้จ้า"
            )
        return cleaned_data 