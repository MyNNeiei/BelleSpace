from datetime import date,datetime
from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, DateInput
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.forms import UserCreationForm
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

class UserDetailLoginForm(ModelForm):
    class Meta:
        model = UsersDetail
        fields = [
            "birth_date",
            "phone_number"
        ]
        widgets = {
            "birth_date" : DateInput(attrs={"type": "date"}),
            }
    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get("hire_date")
        birth_now = datetime.now().date()
        if birth_date > birth_now:
            raise ValidationError(
                    "birth_date ว่าจะต้องไม่เป็นวันในอนาคต"
            )
        return cleaned_data