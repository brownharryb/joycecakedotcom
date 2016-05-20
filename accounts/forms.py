from django import forms
from django.core.exceptions import ValidationError
from mainsite import misc_functions
from django.contrib.auth.models import User
from . import models



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
		all_users_info = models.UserInfo.objects.all()
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


		# *********************Username Check**************
		all_usernames = [x.user.username for x in all_users_info]
		if username in all_usernames:
			raise ValidationError('Username already exists!!')

		# ************************************************

		# ***************Email Check*********************
		if not misc_functions.email_is_ok(email):
			raise ValidationError("Please check your email address!!")
		all_emails = [x.user.email for x in all_users_info]
		if email in all_emails:
			raise ValidationError('That email already exists!!')
		# *************************************************


		# ***************Mobile Number*********************
		if not misc_functions.mobile_number_is_ok(mobile_number):
			raise ValidationError('Invalid Mobile Number')
		all_numbers = [x.mobile_phone for x in all_users_info]
		if mobile_number in all_numbers:
			raise ValidationError('Mobile Number already exists!!')

		
		if not password == verify_password:
			raise ValidationError('Passwords don\'t match!!')

		# ******************************************************

		return self.cleaned_data

class DeliveryForm(forms.Form):
	address1 = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Address 1'}))
	address2 = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Address 2'}), required=False)
	city = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder':'City'}))
	state = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder':'State'}))
	country= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Country'}))

	def get_title(self):
		return 'Delivery Information'

	def clean(self):
		super(DeliveryForm,self).clean()
		address1 = self.cleaned_data.get('address1')
		address2 = self.cleaned_data.get('address2')
		city = self.cleaned_data.get('city')
		state = self.cleaned_data.get('state')
		country = self.cleaned_data.get('country')

		temp_data = {}
		temp_data['Address 1 input'] = address1		
		temp_data['City'] = city
		temp_data['State'] = state
		temp_data['Country'] = country

		emptychar = misc_functions.input_is_not_empty(temp_data)
		if not emptychar==1:
			raise ValidationError('%s is required!!' %emptychar)

		temp_data['Address 2 input'] = address2

		invalidchar = misc_functions.input_is_alpha_numerals(temp_data, space_allowed=True)
		if not invalidchar == 1:
			raise ValidationError('%s is invalid!!' %invalidchar)

		return self.cleaned_data

		


class LoginForm(forms.Form):	
	username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

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
	email = forms.EmailField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Email'}))

	def clean(self):
		super(ForgotPassword, self).clean()
		email = self.cleaned_data.get('email')

		if not email:
			raise ValidationError('Inavlid Email!!')
		else:
			allowed = 'abcdefghijklmnopqrstuvwxyz0123456789_@.'
			for i in email:
				if not i in allowed:
					raise ValidationError('Invalid Email!!')
		return self.cleaned_data


class MyProfileForm(forms.Form):
	full_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Name'}),required=False)
	first_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'Firstname'}))
	last_name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'Lastname'}))
	email = forms.CharField(max_length=20,widget=forms.EmailInput(attrs={'placeholder':'Email'}))
	mobile_number = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'placeholder':'Mobile Number'}))
	username = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Username'}))
	address1 = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Address 1'}))
	address2 = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Address 2'}), required=False)
	city = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder':'City'}))
	state = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder':'State'}))
	country= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Country'}))
	extra_details = forms.CharField(max_length=100,widget=forms.Textarea(attrs={'placeholder':'Extra Details','rows':1}), required=False)

	def clean(self):
		super(MyProfileForm, self).clean()
		all_users_info = models.UserInfo.objects.all()
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		email = self.cleaned_data.get('email')
		mobile_number = self.cleaned_data.get('mobile_number')
		username = self.cleaned_data.get('username')
		address1 = self.cleaned_data.get('address1')
		address2 = self.cleaned_data.get('address2')
		city = self.cleaned_data.get('city')
		state = self.cleaned_data.get('state')
		country = self.cleaned_data.get('country')

		temp_data = {} 
		temp_data['Firstname'] = first_name
		temp_data['Lastname'] = last_name		
		temp_data['Username'] = username
		temp_data['Email'] = email
		temp_data['Mobile Number'] = mobile_number
		temp_data['Address 1 input'] = address1		
		temp_data['City'] = city
		temp_data['State'] = state
		temp_data['Country'] = country

		emptychar = misc_functions.input_is_not_empty(temp_data)
		if not emptychar == 1:
			raise ValidationError('%s is required!' %emptychar)
		temp_data = {} 
		temp_data['Firstname'] = first_name
		temp_data['Lastname'] = last_name
		temp_data['Address 1 input'] = address1
		if address2:
			temp_data['Address 2 input'] = address2
		temp_data['City'] = city
		temp_data['State'] = state
		temp_data['Country'] = country
		
		invalidchar = misc_functions.input_is_alpha_numerals(temp_data, space_allowed=True)
		if not invalidchar == 1:
			raise ValidationError('Invalid %s' %invalidchar)
		
		invaliduser = misc_functions.input_is_alpha_numerals({'Username':username})
		if not invalidchar == 1:
			raise ValidationError('Invalid %s' %invaliduser)
		# ***************Email Check*********************
		if not misc_functions.email_is_ok(email):
			raise ValidationError("Please check your email address!!")
		# *************************************************
		# ***************Mobile Number*********************
		if not misc_functions.mobile_number_is_ok(mobile_number):
			raise ValidationError('Invalid Mobile Number')
		# ******************************************************
		return self.cleaned_data


class ChangePasswordForm(forms.Form):
	first_password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'placeholder':'New Password'}))
	second_password = forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

	def clean(self):
		super(ChangePasswordForm, self).clean()
		p1 = self.cleaned_data.get('first_password')
		p2 = self.cleaned_data.get('second_password')

		if any([p1=='',p2=='',p1==None,p2==None]):
			raise ValidationError('Invalid Password Input!!')
		if not misc_functions.input_is_alpha_numerals({'Password':p1,'Password2':p2})==1:
			raise ValidationError('Invalid Characters in Password!!')
		if not p1 == p2:
			raise ValidationError('Passwords don\'t match!!')

		return self.cleaned_data

