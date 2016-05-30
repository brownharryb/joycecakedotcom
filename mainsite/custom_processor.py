from django.conf import settings
from shop import models as shopmodels
from django.core.urlresolvers import reverse

def default_vals(requests):
	default_vals = {}
	default_vals['main_title'] = settings.SITE_TITLE
	default_vals['main_title_extra'] = ' - '+ default_vals['main_title'] 
	default_vals['mobile_numbers'] = ['+2348655003']
	default_vals['index_title'] = "Online Nigerian Cakes Shop"+ default_vals['main_title_extra']
	default_vals['categories'] = shopmodels.ItemCategory.objects.all()
	return  {'default_vals':default_vals}

def cart_items_function(requests):
	cart_items = requests.session['cart_items']
	cart_items = [int(i) for i in cart_items]
	cart_items_as_string = 'a'.join([str(j) for j in cart_items])
	return {'cart_items':cart_items,'cart_items_string':cart_items_as_string}

def get_navlinks(requests):
	nav_links = {}
	nav_links[1] = ['home',reverse('home_url')]
	nav_links[2] = ['gallery',reverse('shop-gallery-view')]
	nav_links[3] = ['contact us',reverse('contact_us_url')]
	return {'nav_links':nav_links}