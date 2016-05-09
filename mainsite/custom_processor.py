from django.conf import settings
from shop import models as shopmodels

def default_vals(requests):
	default_vals = {}
	default_vals['main_title'] = settings.SITE_TITLE
	default_vals['main_title_extra'] = ' - '+ default_vals['main_title'] 
	default_vals['mobile_numbers'] = ['+2348655003']
	default_vals['index_title'] = "Online Nigerian Cakes Shop"+ default_vals['main_title_extra']
	default_vals['categories'] = shopmodels.ItemCategory.objects.all()
	return  {'default_vals':default_vals}