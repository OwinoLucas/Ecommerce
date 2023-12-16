from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm


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
    class Meta:
        model = Customer
        fields=['mobile','profile_pic']