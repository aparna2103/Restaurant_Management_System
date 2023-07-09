from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    full_name = forms.CharField(required=True)

    class Meta:
        model = UserTable
        fields = ["full_name","username", "email", "password1", "password2", "address", "contact_number"]

class UserPaymentDetails(forms.ModelForm):
 
    class Meta:
        model = UserPaymentInformation
        fields = ['cardnumber', 'cvv']