from django import forms
from django.core.exceptions import ValidationError
from mainsite import misc_functions
from django.contrib.auth.models import User



class RegisterForm(forms.Form):
	first_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'Firstname'}))
	last_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'Lastname'}))
	email = forms.CharField(max_length=20,widget=forms.EmailInput(attrs={'placeholder':'Email'}))
	mobile_number = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'Mobile Number'}))
	username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
	verify_password= forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'placeholder':'Verify Password'}))

	def get_title(self):
		return 'Register'


	def clean(self):
		super(RegisterForm, self).clean()
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		email = self.cleaned_data.get('email')
		mobile_number = self.cleaned_data.get('mobile_number')
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		verify_password = self.cleaned_data.get('verify_password')

		temp_data = {} 
		temp_data['Firstname'] = first_name
		temp_data['Lastname'] = last_name		
		temp_data['Username'] = username
		temp_data['Password'] = password
		temp_data['Verify Password Input'] = verify_password
		temp_data['Email'] = email
		temp_data['Mobile Number'] = mobile_number

		emptychar = misc_functions.input_is_not_empty(temp_data)
		if not emptychar == 1:
			raise ValidationError('%s is required!' %emptychar)

		temp_data = {} 
		temp_data['Firstname'] = first_name
		temp_data['Lastname'] = last_name


		invalidchar = misc_functions.input_is_alpha_numerals(temp_data, space_allowed=True)
		if not invalidchar == 1:
			raise ValidationError('Invalid %s' %invalidchar)
		
		invaliduser = misc_functions.input_is_alpha_numerals({'Username':username, 'Password':password,
																'Verify Password Input':verify_password})
		if not invalidchar == 1:
			raise ValidationError('Invalid %s' %invaliduser)

		if not misc_functions.email_is_ok(email):
			raise ValidationError("Please check your email address!!")

		print 'mobile number is = '+str(mobile_number)

		if not misc_functions.mobile_number_is_ok(mobile_number):
			raise ValidationError('Invalid Mobile Number')

		if not password == verify_password:
			raise ValidationError('Passwords don\'t match!!')

		return self.cleaned_data


		


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
		invalidchar = misc_functions.input_is_alpha_numerals({'Username':username, 'Password':password})
		if not invalidchar == 1:
			raise ValidationError('Invalid %s' %invalidchar)
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
