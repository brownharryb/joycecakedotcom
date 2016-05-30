from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.views.generic import View, FormView
from . import models
from accounts import models as accountsmodels
from accounts import forms as accountsforms
from mainsite.misc_functions import confirm_sessions_and_cookies,get_proper_fullname,decode_session_string
from mainsite import misc_functions
import random,json


#********************************Gallery*****************
@confirm_sessions_and_cookies
def gallery_view(requests):
	# try:
	cat = models.ItemCategory.objects.get(pk=1)
	cakes = models.Item.objects.filter(category=cat)
	cakes = list(cakes)
	cakes = randomize_list(cakes)
	return render(requests,'gallery.html',{'cakes':cakes})
	# except:
		# return render(requests,'page404.html')

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
		extra_images = item.get_extra_images()
		gifts = get_random_gift_items()
		return render(requests,'itemdetail.html',{'item':item,'gifts':gifts,'extra_images':extra_images})
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
# @confirm_sessions_and_cookies
def toggle_cart_view(requests,item_id):
	response_items = {}

	# TODO FIX THIS
	
	# try:
	item_id = int(item_id)
	item = models.Item.objects.get(pk=item_id)
	response_items['item_id'] = item_id

	if item.is_in_cart(requests):
		response_items['available'] = True
		requests = item.remove_from_cart(requests)

		response_items['button_text'] = 'Add To Cart'
	else:
		response_items['available'] = False
		requests = item.add_to_cart(requests)
		response_items['button_text'] = 'Added'

	response_items['all_items'] = requests.session['cart_items']
	response_items['items_length'] = len(response_items['all_items'])

	j = json.dumps(response_items)
	return HttpResponse(j)
	# except:
		# return render(requests,'page404.html')

def confirm_item_price(requests, item_id):
	item_id = int(item_id)
	item = models.Item.objects.get(pk=item_id)
	return HttpResponse(item.sale_price)


def confirm_selected_item_prices(requests,item_ids_string):
	sale_prices = {}



	item_id_list = item_ids_string
	item_id_list = [int(i) for i in item_id_list if not i == 'a']
	all_items = models.Item.objects.filter(id__in=item_id_list)
	for j in all_items:
		sale_prices[j.id] = j.sale_price
	return HttpResponse(json.dumps(sale_prices))



class CartView(View):
	template_name = 'cart.html'
	initial = {}
	profile_form_class = accountsforms.MyProfileForm
	gifts = ''

	@confirm_sessions_and_cookies
	def dispatch(self,requests,*args,**kwargs):
		self.gifts = get_random_gift_items()
		return super(CartView,self).dispatch(requests,*args,**kwargs)

	def get(self,requests,*args,**kwargs):
		totalprice = 0
		all_ids =  [int(i) for i in requests.session.get('cart_items')]
		all_cart_items = models.Item.objects.filter(id__in=all_ids)
		for j in all_cart_items:
			totalprice+=j.sale_price

		return render(requests,'cart.html',{'gifts':self.gifts,'all_cart_items':all_cart_items,'totalprice':totalprice})
	def post(self,requests,*args,**kwargs):
		item_session_string = ''
		if not requests.user.is_authenticated():
			url = reverse('user_login')
			cart_url = reverse('shop-cart-view')
			url+='?next=%s'%(cart_url)
			return redirect(url)
		totalprice = 0			
		returndict = {}
		post_data = requests.POST
		all_data_keys = requests.POST.keys()
		all_data_ids = requests.session.get('cart_items')
		if all_data_ids == []:
			return render(requests,'cart.html',{'gifts':self.gifts,'all_cart_items':all_cart_items,'totalprice':totalprice})
		
		for i in all_data_keys:
			j = i.split('_')
			if 'id' in j:
				id_num = int(j[1])
				item = models.Item.objects.get(pk=id_num)
				# TODO MAKE A SESSION STRING TO STORE ALL QTY, ID,SINGLE PRICE AND TOTAL PRICE					
				price = item.sale_price * int(post_data[i])
				item_session_string += '_i{0}|q{1}|p{2}'.format(id_num, post_data[i], price)
				returndict[id_num] = price
				totalprice+=price
		requests.session['totalprice_in_cart'] = totalprice
		requests.session['order_string'] = item_session_string		
		form = self.prepareform(requests)
		return render(requests,'checkout.html',{'gifts':self.gifts,'datadict':returndict,'totalprice':totalprice,'profile_form':form})

	# def flag_is_ok(self,flag):
	# 	allowedchars = 'abcdefghijklmnopqrstuvwxyz0123456789/'
	# 	for i in flag:
	# 		if not i in allowedchars:
	# 			return False
	# 	return True
	

	def prepareform(self,requests):		
		cart_items = requests.session.get('cart_items')
		cart_items = [models.Item.objects.get(pk=int(i)) for i in cart_items]
		user = requests.user
		user_info = accountsmodels.UserInfo.objects.get(user=user)

		self.initial['first_name'] = user.first_name
		self.initial['last_name'] = user.last_name
		self.initial['username'] = user.username
		self.initial['email'] = user.email
		self.initial['full_name'] = get_proper_fullname(user.get_full_name())
		self.initial['mobile_number'] = user_info.mobile_phone
		self.initial['address1'] = user_info.delivery_address1
		self.initial['address2'] = user_info.delivery_address2
		self.initial['city'] = user_info.city
		self.initial['state'] = user_info.state
		self.initial['country'] = user_info.country

		profile_form = self.profile_form_class(self.initial)
		return profile_form


def success_order_view(request):
	return render(request, 'success_order.html')



class CheckoutView(View):
	success_template = 'success_order.html'
	fail_template = 'fail_order.html'

	def post(self,requests,*args,**kwargs):
		item_ids = []
		order_string = requests.session.get('order_string')
		items_list =  decode_session_string(order_string)
		totalprice = requests.session.get('totalprice_in_cart')
		for i in items_list:
			item_ids.append(int(i['item_id']))
		all_items = models.Item.objects.filter(id__in=item_ids)
		user_transaction = accountsmodels.UserTransaction()
		user_transaction.user= accountsmodels.UserInfo.objects.get(user=requests.user)
		user_transaction.session_string = order_string
		user_transaction.save()
		for i in all_items:
			user_transaction.items.add(i)
		user_transaction.save()
		requests.session['cart_items'] = []
		self.send_mail_to_alert_webmaster(requests,user_transaction,items_list)
		self.send_confirm_mail_to_customer()	
		return render(requests,self.success_template)
		
	# TODO SEND MAIL
	def send_mail_to_alert_webmaster(self,request,user_transaction,items_list):
		totalprice = 0
		user_info =  user_transaction.user
		user = user_info.user
		items = user_transaction.items.all()
		contact_str = 'Name: {0}\nMobile:{1} \nEmail:{2}'.format(misc_functions.get_proper_fullname(user.get_full_name()),
												user_info.mobile_phone,user.email)
		add_str = 'Address:  {0}\n{1}\n{2}\n{3}'.format(user_info.delivery_address1,
								user_info.delivery_address2,user_info.city, user_info.state)
		msg = 'Transaction Notification:\n\n'
		for i in items_list:
			each_item = models.Item.objects.get(pk=int(i['item_id']))
			item_name = each_item.name
			item_link = each_item.get_full_item_detail_link(request)
			sale_price = each_item.get_sale_price(i['item_qty'])
			totalprice +=sale_price
			msg+='\nName:'+str(item_name)+'  Qty:'+str(i['item_qty'])+'  Link:'+str(item_link)+' Price:'+str(sale_price)

		msg+='\n\nTotal Price:{0}'.format(totalprice)
		msg +='\n\n\n\n{0}'.format(contact_str)
		msg += ' \n\n{0}'.format(add_str)

		msg +=' \n\n\nRegards \nJoycecake.com.'


		subject_text='Transaction Notification on Joycecake.com'
		my_email=settings.MY_EMAIL_ADDRESS
		recipients=[settings.MY_EMAIL_ADDRESS]
		# misc_functions.send_email(subject_text,recipients,msg)
		print 'Msg = {0}'.format(msg)

	def send_confirm_mail_to_customer(self):
		pass

	