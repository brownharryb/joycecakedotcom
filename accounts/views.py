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
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			mobile_number = form.cleaned_data['mobile_number']
			username = form.cleaned_data['username']
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
	initial = {'key':'value'}


	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect(reverse('user_register'))
		return super(UserDeliveryView, self).dispatch(request, *args, **kwargs)


	def get(self,request,*args,**kwargs):
		form = self.form_class(initial={'city':'Port Harcourt','state':'Rivers','country':'Nigeria'})
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

	def get(self,request,*args,**kwargs):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form':form})

	def post(self,request,*args,**kwargs):
		form = self.form_class(request.POST)

		if form.is_valid():			
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
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

