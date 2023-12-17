from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django_countries.widgets import CountrySelectWidget
from .validators import validate_possible_number

class UserRegisterForm(UserCreationForm):

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']
			


class LoginForm(forms.Form):

    username = forms.CharField(label="Username")
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class CustomerUpdateForm(forms.ModelForm):
    mobile = PhoneNumberField(validators=[validate_possible_number])
    class Meta:
        model = Customer
        fields=[ 'mobile','profile_pic']
        
        