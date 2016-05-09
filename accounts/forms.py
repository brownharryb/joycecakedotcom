from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):	
	username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

	def get_title(self):
		return 'Login'

	def clean(self):
		super(LoginForm, self).clean()
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if not username or not password:
			raise ValidationError('Empty Username Or Password!!')
		else:
			allowed = 'abcdefghijklmnopqrstuvwxyz0123456789_'
			for i in [username,password]:
				for j in i:
					if not j in allowed:
						raise ValidationError('Invalid Username Or Password!!')
		return self.cleaned_data




class ForgotPassword(forms.Form):
	email = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Email'}))

	def clean(self):
		super(ForgotPassword, self).clean()
		email = self.cleaned_data.get('email')

		if not email:
			raise ValidationError('Empty Email')
		else:
			allowed = 'abcdefghijklmnopqrstuvwxyz0123456789_@.'
			for i in email:
				if not i in allowed:
					raise ValidationError('Invalid Email!!')
		return self.cleaned_data
