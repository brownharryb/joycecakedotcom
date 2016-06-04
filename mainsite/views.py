from django.shortcuts import render
from django.conf import settings
from shop import models as shopmodels
from misc_functions import confirm_sessions_and_cookies
from django.views.generic import View
from misc_functions import randomize_list




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
		featured_items = randomize_list(list(shopmodels.Item.objects.filter(featured=True)[:self.carousel_length]))
		wedding_cakes = randomize_list(list(shopmodels.Item.objects.filter(category=self.wedding_category)[:self.carousel_length]))
		birthday_cakes = randomize_list(list(shopmodels.Item.objects.filter(category=self.birthday_category)[:self.carousel_length]))
		self.carousel_items[1] = ['Featured',featured_items,False]#boolean for "view all links" button
		self.carousel_items[2] = ['Wedding Cakes',wedding_cakes,True]
		self.carousel_items[3] = ['Birthday Cakes',birthday_cakes,True]
		return render(requests,self.template_name,{'carousel_items':self.carousel_items})

@confirm_sessions_and_cookies
def contact_us_view(requests):
	return render(requests,'contact_us.html')

			