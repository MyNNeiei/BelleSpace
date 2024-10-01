from datetime import date,datetime
from django import forms
from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, DateInput
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        ]
class UserdetailRegisterForm(forms.ModelForm):
    class Meta:
        model = UsersDetail
        fields = [
            'gender',
            'phone_number',
            'birth_date',
            'image_profile'
        ]
    def clean_birthdate(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get("birth_date")
        birth_now = datetime.now().date()
        if birth_date > birth_now:
            raise ValidationError(
                    "birth_date ว่าจะต้องไม่เป็นวันในอนาคต"
            )
        return cleaned_data
    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        
        data = UsersDetail.objects.filter(phone_number = phone_number)
        if data.count():
            raise ValidationError("Phone number Already Exist")
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValidationError("เบอร์โทรศัพท์ควรมีแค่10 ตัวเลข")
        return phone_number

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
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    service_name = forms.CheckboxSelectMultiple()
    class Meta:
        model = Appointment
        fields = [
            "first_name",
            "last_name",
            "category", 
            "staff",
            "appointment_date",
        ]
        # model = User
        # fields = [
        #     "first_name",
        #     "last_name",

        # ]

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