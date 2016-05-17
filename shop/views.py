from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.views.generic import View, FormView
from . import models
from mainsite.misc_functions import confirm_sessions_and_cookies
import random


#********************************Gallery*****************
@confirm_sessions_and_cookies
def gallery_view(requests):
	try:
		cat = models.ItemCategory.objects.get(pk=1)
		cakes = models.Item.objects.filter(category=cat)
		cakes = list(cakes)
		cakes = randomize_list(cakes)
		return render(requests,'gallery.html',{'cakes':cakes})
	except:
		return render(requests,'page404.html')

@confirm_sessions_and_cookies
def gallery_view_with_category(requests,category_slug):
	try:
		cat = models.ItemCategory.objects.get(slug=category_slug)
		cakes = models.Item.objects.filter(category=cat)
		cakes = list(cakes)
		cakes = randomize_list(cakes)
		return render(requests,'gallery.html',{'cakes':cakes})
	except:
		return render(requests,'page404.html')
#************************************************************
# ********************************Item Detail************************
# TODO WORK ON CART
@confirm_sessions_and_cookies
def item_detail_view(requests,item_category,item_slug):
	try:
		category = models.ItemCategory.objects.get(slug=item_category)
		item = models.Item.objects.get(slug=item_slug, category=category)
		gifts = get_random_gift_items()
		return render(requests,'itemdetail.html',{'item':item,'gifts':gifts})
	except:
		return render(requests,'page404.html')

def get_random_gift_items():
	gift_category = models.ItemCategory.objects.filter(item_type='2')
	gifts = []
	for i in gift_category:
		temp_gifts = models.Item.objects.filter(category=i)
		for j in temp_gifts:
			gifts.append(j)
	gifts = randomize_list(gifts)
	return gifts

def randomize_list(list_obj):
	new_list = []
	while not list_obj == []:
		rdm = random.choice(list_obj)
		new_list.append(rdm)
		list_obj.remove(rdm)
	return new_list


# ***************************************************************************
# *******************************CART DETAIL *******************************
# TODO MODIFY TO RETURN JSON
def add_to_cart_view(requests,item_id):
	try:
		item_id = int(item_id)
		item = models.Item.objects.get(pk=item_id)
		if item.is_in_cart(requests):
			return HttpResponse('available')
		item.add_to_cart(requests)
		all_items = requests.session['cart_items']
		return HttpResponse('added')
	except:
		return render(requests,'page404.html')
		
def remove_from_cart_view(requests,item_id):
	try:
		item_id = int(item_id)
		item = models.Item.objects.get(pk=item_id)
		if item.is_in_cart(requests):
			item.remove_from_cart(requests)
			return HttpResponse('removed')
		return HttpResponse('notavailable')
	except:
		return render(requests,'page404.html')

class CartView(View):
	template_name = 'cart.html'

	@confirm_sessions_and_cookies
	def dispatch(self,requests,*args,**kwargs):
		return super(CartView,self).dispatch(requests,*args,**kwargs)

	def get(self,requests,*args,**kwargs):
		totalprice = 0
		all_ids =  [int(i) for i in requests.session.get('cart_items')]
		all_cart_items = models.Item.objects.filter(id__in=all_ids)
		for j in all_cart_items:
			totalprice+=j.sale_price

		return render(requests,'cart.html',{'all_cart_items':all_cart_items,'totalprice':totalprice})
# **************************************************************************
class CheckoutView(View):
	template_name = 'checkout.html'

	@confirm_sessions_and_cookies
	def dispatch(self,requests,*args,**kwargs):
		if not requests.user.is_authenticated():
			url = reverse('user_login')
			checkout_url = reverse('shop-checkout-view')
			url+='?next=%s'%(checkout_url)
			return redirect(url)
		return super(CheckoutView,self).dispatch(requests,*args,**kwargs)

	def get(self,requests,*args,**kwargs):
		return render(requests,self.template_name)
