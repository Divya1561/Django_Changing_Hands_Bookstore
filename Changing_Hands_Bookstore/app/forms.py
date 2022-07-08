from dataclasses import fields
import email
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from matplotlib import widgets
from matplotlib.pyplot import cla
from django.contrib.auth import password_validation

from .models import Contact, Customer, Product


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

class Meta:
    model = User
    fields = ['username', 'password1', 'password2', 'email']
    labels = {'email': 'Email'}
    widgets = {'username': forms.TextInput(attrs={'class': 'form-control'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    password =forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs= {'autocomplete': 'current-password', 'autofocus':True, 'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs= {'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs= {'autocomplete': 'new-password', 'class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {'name':forms.TextInput(attrs= {'class':'form-control'}), 'locality':forms.TextInput(attrs= {'class':'form-control'}), 'city':forms.TextInput(attrs= {'class':'form-control'}), 'state':forms.Select(attrs= {'class':'form-control'}), 'zipcode':forms.NumberInput(attrs= {'class':'form-control'})}



class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'mobileno', 'message']
        widgets = {'name':forms.TextInput(attrs= {'class':'form-control'}), 'email':forms.EmailInput(attrs= {'class':'form-control'}), 'mobileno':forms.NumberInput(attrs= {'class':'form-control'}), 'message':forms.TextInput(attrs= {'class':'form-control'})}


class MySellForm(forms.ModelForm):
    class Meta:
        model = Product
        fields= ['title','selling_price', 'discounted_price', 'description', 'author', 'category', 'type', 'product_image']
        widgets={'title':forms.TextInput(attrs= {'class':'form-control'}),'selling_price':forms.NumberInput(attrs= {'class':'form-control'}),'discounted_price':forms.NumberInput(attrs= {'class':'form-control'}),'description':forms.TextInput(attrs= {'class':'form-control'}),'author':forms.TextInput(attrs= {'class':'form-control'}),'category':forms.Select(attrs= {'class':'form-control'}),'type':forms.Select(attrs= {'class':'form-control'})}


