from django.shortcuts import render , redirect
from django.core.urlresolvers import reverse
from django.views.generic import View, FormView
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from . import forms,models






class UserRegister(FormView):
	template_name = 'register.html'
	form_class = forms.RegisterForm
	initial = {'key':'value'}

	def get(self, request, *args, **kwargs):
		form = self.form_class(initial=self.initial)
		return render(request,self.template_name, {'form':form})

	def post(self,request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data['first_name'].lower()
			last_name = form.cleaned_data['last_name'].lower()
			email = form.cleaned_data['email'].lower()
			mobile_number = form.cleaned_data['mobile_number'].lower()
			username = form.cleaned_data['username'].lower()
			password = form.cleaned_data['password']

			user = User(first_name=first_name, last_name =last_name, email=email,
						username=username)
			user.set_password(password)
			user.save()
			user_info = models.UserInfo(user=user,mobile_phone=mobile_number)
			user_info.save()
			return redirect(reverse('user_delivery'))
		else:
			return render(request,self.template_name, {'form':form})

class UserDeliveryView(View):
	template_name = 'delivery_form.html'
	form_class = forms.DeliveryForm
	initial={'city':'Port Harcourt','state':'Rivers','country':'Nigeria'}


	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect(reverse('user_register'))
		return super(UserDeliveryView, self).dispatch(request, *args, **kwargs)


	def get(self,request,*args,**kwargs):
		try:
			user_info = models.UserInfo.objects.get(user=request.user)
			if user_info.delivery_address1:
				self.initial['address1'] = user_info.delivery_address1
			if user_info.delivery_address2:
				self.initial['address2'] = user_info.delivery_address2
			if user_info.city:
				self.initial['city'] = user_info.city
			if user_info.state:
				self.initial['state'] = user_info.state
			if user_info.country:
				self.initial['country'] = user_info.country
		except:
			initial={'city':'Port Harcourt','state':'Rivers','country':'Nigeria'}
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name,{'form':form})

	def post(self,request,*args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			return render(request,'success.html')
		else:
			return render(request, self.template_name,{'form':form})	


class UserLogin(View):
	template_name = 'login.html'
	form_class = forms.LoginForm
	initial = {'key':'value'}

	# def dispatch(self,request,*args,**kwargs):
	# 	print "user = "+str(request.user.is_authenticated())
	# 	if request.user.is_authenticated():
	# 		return redirect(reverse('home_url'))		
	# 	return super(UserLogin, self).dispatch(request,*args,**kwargs)

	def get(self,request,*args,**kwargs):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form':form})

	def post(self,request,*args,**kwargs):
		form = self.form_class(request.POST)

		if form.is_valid():			
			username = form.cleaned_data['username'].lower()
			password = form.cleaned_data['password'].lower()
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return render(request,'success.html', {'form':form})
				# else:
				# 	return render(request, 'fail.html', {'form':form})
			else:
				form.add_error(None,ValidationError('Invalid Username Or Password!!'))
				return render(request, self.template_name, {'form':form})


		else:
			return render(request, self.template_name, {'form':form})

class ForgotPassword(View):
	template_name = 'forgotpass.html'
	form_class = forms.ForgotPassword
	initial = {'key':'value'}

	def get(self,request,*args, **kwargs):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form':form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)

		if form.is_valid():
			email = form.cleaned_data['email']
			
		else:
			return render(request, self.template_name, {'form':form})

class UserProfileView(View):
	template_name = 'user_profile.html'
	form_class = forms.MyProfileForm
	form_initial = {}
	user = ''
	user_info = ''
	username = ''

	def dispatch(self,request,*args,**kwargs):
		if not request.user.is_authenticated():
			return redirect(reverse('home_url'))
		try:
			self.user = request.user
			self.user_info = models.UserInfo.objects.get(user=self.user)
			self.username = self.user.username
			self.all_other_users = User.objects.exclude(username=self.username)
			self.all_other_users_info = models.UserInfo.objects.exclude(user=self.user)
		except:
			return render(request, 'page404.html')			
		return super(UserProfileView, self).dispatch(request, *args, **kwargs)


	def get(self,request,*args,**kwargs):
		try:			
			self.form_initial['first_name'] = self.user.first_name.capitalize()
			self.form_initial['last_name'] = self.user.last_name.capitalize()
			self.form_initial['email'] = self.user.email
			self.form_initial['username'] = self.user.username
			self.form_initial['mobile_number'] = self.user_info.mobile_phone
			self.form_initial['address1'] = self.user_info.delivery_address1
			self.form_initial['city'] = self.user_info.city
			self.form_initial['state'] = self.user_info.state
			self.form_initial['country'] = self.user_info.country
			if self.user_info.delivery_address2:
				self.form_initial['address2'] = self.user_info.delivery_address2
		except:
			self.form_initial={'key':'value'}

		form = self.form_class(initial=self.form_initial)
		return render(request, self.template_name, {'form':form})

	def post(self,request,*args,**kwargs):
		form = self.form_class(request.POST)



		if form.is_valid():
			if form.has_changed():
				self.user.first_name = form.cleaned_data['first_name'].lower()
				self.user.last_name = form.cleaned_data['last_name'].lower()


				if not list(self.all_other_users.filter(email=form.cleaned_data['email'].lower()))==[]:
					form.add_error(None,ValidationError('Email already exists!!'))
					return render(request, self.template_name, {'form':form})
				self.user.email = form.cleaned_data['email'].lower()

				if not list(self.all_other_users.filter(username=form.cleaned_data['username'].lower()))==[]:
					form.add_error(None,ValidationError('Username already exists!!'))
					return render(request, self.template_name, {'form':form})
				self.user.username = form.cleaned_data['username'].lower()

				if not list(self.all_other_users_info.filter(mobile_phone=form.cleaned_data['mobile_number'].lower()))==[]:
					form.add_error(None,ValidationError('Phone Number already exists!!'))
					return render(request, self.template_name, {'form':form})
				self.user_info.mobile_phone = form.cleaned_data['mobile_number'].lower()
							
				
				self.user_info.delivery_address1= form.cleaned_data['address1'].lower()
				if form.cleaned_data['address2']:
					self.user_info.delivery_address2 = form.cleaned_data['address2'].lower()
				self.user_info.city = form.cleaned_data['city']
				self.user_info.state = form.cleaned_data['state']
				self.user_info.country = form.cleaned_data['country']



				self.user.save()
				self.user_info.save()
			return render(request, 'success.html')
		else:
			return render(request, self.template_name, {'form':form})

	def check_duplicate_username_available(self,username):
		if self.username == username:
			return False
		try:
			username = User.objects.get(username=username)
			if username:
				return True
		except:
			return False