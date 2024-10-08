from datetime import date,datetime
from django import forms
from django.forms import DateTimeInput, EmailInput, ModelForm, PasswordInput, Select, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, DateInput
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

        
from django.utils import timezone
class UserRegisterForm(UserCreationForm):
    GENDER_CHOICES = [
        ("", "เลือกเพศ"),
        ("M", "Male"),
        ("F", "Female"),
        ("LGBTQ", "LGBTQ+"),
        ("O", "Others"),
    ]
    gender = forms.ChoiceField(required=False, choices=GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'}))
    phone_number = forms.CharField(max_length=10,
                                   widget=forms.TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'กรอกเบอร์โทรศัพท์'}))
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class" : "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"})
    )
    # image_profile = forms.ImageField()
    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
            "email",
            "first_name",
            "last_name",
            "gender",
            "phone_number",
            "birth_date",
        ]
        widgets = {
            "username" : TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'Username'}),
            "password1" : PasswordInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'Password'}),
            "password2" : PasswordInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'Confirm Password'}),
            "email" : EmailInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'Username'}),
            "first_name" : TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'First_name'}),
            "last_name" : TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'Last_name'}),
            # "birth_date" : DateInput(attrs={"type": "date", "class" : "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"}),
            # "gender" : Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'}),
            # "phone_number" : TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'กรอกเบอร์โทรศัพท์'}),
        }
    def clean_birthdate(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get("birth_date")
        birth_now = datetime.now().date()
        if birth_date > birth_now and birth_date == birth_now:
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

class EditProfileForm(forms.ModelForm):
    GENDER_CHOICES = [
        ("", "เลือกเพศ"),
        ("M", "Male"),
        ("F", "Female"),
        ("LGBTQ", "LGBTQ+"),
        ("O", "Others"),
    ]
    gender = forms.ChoiceField(required=False, choices=GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'}))
    phone_number = forms.CharField(max_length=10,
                                   widget=forms.TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'กรอกเบอร์โทรศัพท์'}))
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class" : "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"})
    )
    image_profile = forms.ImageField()
    class Meta:
        model = User
        fields = ['first_name', 
                  'last_name', 
                  'email',
                  'gender',
                  'phone_number',
                  'birth_date',
                  'image_profile',
                  ]  # Add other fields as needed
        widgets = {
            "username" : TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'Username'}),
            "email" : EmailInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'Username'}),
            "first_name" : TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'First_name'}),
            "last_name" : TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'Last_name'}),
            "birth_date" : DateInput(attrs={"type": "date", "class" : "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"}),
            "gender" : Select(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full'}),
            "phone_number" : TextInput(attrs={'class': 'border border-gray-300 rounded px-3 py-2 w-full', 'placeholder': 'กรอกเบอร์โทรศัพท์'}),
        }
    def clean_birthdate(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get("birth_date")
        birth_now = datetime.now().date()
        if birth_date > birth_now and birth_date == birth_now:
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
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
# class AppointmentForm(forms.ModelForm):
#     # staff_id = forms.ModelChoiceField(
#     #     queryset=Staff.objects.all(),
#     #     required=True,
#     #     label='พนักงาน'
#     # )

#     services = forms.ModelChoiceField(
#         queryset=Service.objects.all(),
#         widget=forms.SelectMultiple(attrs={
#             'class': 'text-[#74342B] text-xl rounded scale-[1.2] my-3 ml-5', 
#         }),
#         required=True,
#         label='บริการ',
#     )

#     class Meta:
#         model = Appointment
#         fields = [
#                 'category',
#                 'services', 
#                 'appointment_date',
#                 ]
#         labels = {
#             'appointment_date': 'วันที่นัดหมาย',
#             }
#         data = UsersDetail.objects.filter(phone_number = phone_number)
#         if data.count():
#             raise ValidationError("Phone number Already Exist")
#         if len(phone_number) != 10 or not phone_number.isdigit():
#             raise ValidationError("เบอร์โทรศัพท์ควรมีแค่10 ตัวเลข")
#         return phone_number

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


# class AppointmentForm(forms.ModelForm):
#     # staff_id = forms.ModelChoiceField(
#     #     queryset=Staff.objects.all(),
#     #     required=True,
#     #     label='พนักงาน'
#     # )
#     services = forms.ModelMultipleChoiceField(
#         queryset=Service.objects.all(),
#         widget=forms.CheckboxSelectMultiple(attrs={
#             'class': 'text-[#74342B] text-xl rounded scale-[1.2] my-3 ml-5', 
#         }),
#         required=True,
#         label='บริการ',
#     )

#     class Meta:
#         model = Appointment
#         fields = [
#                 'services', 
#                 'appointment_date',

#                 ]
#         labels = {
#             'appointment_date': 'วันที่นัดหมาย',
        

#         }
#         widgets = {
#             'appointment_date': DateInput(attrs={
#                 'type': 'date',
#                 'class': 'p-2 rounded-md scale-[1.2] ml-6 text-xl'
                
#             }),
        
            
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         app_date = cleaned_data.get('appointment_date')
#         now = timezone.now()

#         if app_date and app_date < now:
#             raise ValidationError("จองย้อนไม่ได้จ้า")
        
#         return cleaned_data
    
class AppointmentDetailForm(ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "staff_id"
        ]  
    def clean(self):
        cleaned_data = super().clean()

        staff = cleaned_data.get("staff_id")
        return cleaned_data


class AppointmentForm(ModelForm):
    class Meta:
        model = Appointment  # Set model to Appointment
        fields = ['category', 'appointment_date']  # Include the required fields

        labels = {
            'appointment_date': 'วันที่นัดหมาย',  # Appointment date label
        }

        widgets = {
            'appointment_date': DateTimeInput(attrs={
                'type': 'datetime-local',  # Use 'datetime-local' for date and time selection
                'class': 'p-2 rounded-md scale-[1.2] ml-6 text-xl',  # Custom styles
            }),
        }

    category = forms.ModelChoiceField(
        queryset=Categories.objects.all(),
        widget=forms.Select(attrs={"hx-get": "load_services/", "hx-target": "#id_service"})
    )

    service = forms.ModelChoiceField(queryset=Service.objects.none())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "category" in self.data:
            category_id = int(self.data.get("category"))
            self.fields["service"].queryset = Service.objects.filter(category_id=category_id)
        else:
            self.fields["service"].queryset = Service.objects.none()
