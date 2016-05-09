from django.shortcuts import render
from django.conf import settings
from shop import models as shopmodels



def index_view(requests):
	index_view = ''
	index_object = IndexObject()
	return render(requests,"index.html",{'index_object':index_object})	


class IndexObject(object):	
	


	def __init__(self):
		self.number_to_display = 7
		featured_cakes_carousel = self.get_carousel_cakes(tag='featured')
		wedding_cakes = self.get_carousel_cakes(cake_category='Wedding cakes',idnum=2)
		birthday_cakes = self.get_carousel_cakes(cake_category='Birthday cakes',idnum=3)
		self.carousel_items = [featured_cakes_carousel,birthday_cakes,wedding_cakes]



	def get_carousel_cakes(self,cake_category='',tag='category',idnum=1):
		carousel_title = ''
		carousel_cakes = []
		idnum = idnum
		show_view_all_link = True
		if tag == 'featured':
			show_view_all_link = False
			carousel_title = 'Featured Cakes'
			carousel_items = shopmodels.Item.objects.filter(featured=True)[:self.number_to_display]
		elif tag=='category' and not cake_category == '':
			cat_name = shopmodels.ItemCategory.objects.get(name=cake_category)
			carousel_items = shopmodels.Item.objects.filter(category=cat_name)[:self.number_to_display]
			carousel_title = cake_category


		for i in carousel_items:
			item = CarouselItem(item_name=i.name,
								is_new=i.show_as_new,
								old_price=i.old_price,
								sale_price=i.sale_price,
								image_link=i.image_file.url,
								category=i.category,
								item_link_slug='shop/'+i.category.slug+'/'+i.slug)
			carousel_cakes.append(item)
		return {'idnum':idnum,'name':carousel_title,'content':carousel_cakes,'show_view_all_link':show_view_all_link}



		



		
	

class CarouselItem(object):
	item_name = ''
	is_new = False
	old_price = 0
	sale_price = 0
	item_link_slug = ''
	image_link = ''
	category = ''

	def __init__(self,item_name='',
				is_new=False,
				old_price=0,
				sale_price=0,
				item_link_slug='#',
				image_link='',
				category=''):
		self.item_name = item_name
		self.is_new = is_new
		self.old_price = old_price
		self.sale_price = sale_price
		self.item_link_slug = item_link_slug
		self.category = category
		self.image_link = image_link