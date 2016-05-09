from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from . import forms


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

