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