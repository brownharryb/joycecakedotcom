from django.shortcuts import render
from django.conf import settings
from shop import models as shopmodels
from misc_functions import confirm_sessions_and_cookies
from django.views.generic import View




class IndexView(View):
	template_name = 'index.html'
	carousel_length = 7
	carousel_items = {}


	@confirm_sessions_and_cookies
	def dispatch(self,requests,*args,**kwargs):
		self.wedding_category = shopmodels.ItemCategory.objects.get(name='Wedding cakes')
		self.birthday_category = shopmodels.ItemCategory.objects.get(name='Birthday cakes')
		return super(IndexView, self).dispatch(requests,*args,**kwargs)

	def get(self,requests, *args, **kwargs):
		self.carousel_items[1] = ['Featured',shopmodels.Item.objects.filter(featured=True)[:self.carousel_length],False]#boolean for "view all links" button
		self.carousel_items[2] = ['Wedding Cakes',shopmodels.Item.objects.filter(category=self.wedding_category)[:self.carousel_length],True]
		self.carousel_items[3] = ['Birthday Cakes',shopmodels.Item.objects.filter(category=self.birthday_category)[:self.carousel_length],True]
		return render(requests,self.template_name,{'carousel_items':self.carousel_items})




			