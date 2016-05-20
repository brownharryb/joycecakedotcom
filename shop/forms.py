from django import forms
from django.contrib.auth.models import User
from accounts.models import UserInfo

class CheckoutContactForm(forms.Form):
	fullname = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Name'}))
	mobile = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Mobile Number'}))