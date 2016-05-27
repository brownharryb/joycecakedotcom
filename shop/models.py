from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import os, datetime
from mainsite import misc_functions
from django.conf import settings
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.urlresolvers import reverse


def get_image_upload_path(instance, filename):
	cat = str(instance.category)
	cat = cat.replace(' ','_').lower()
	return os.path.join('photos', cat, filename)

def get_extra_images_upload_path(instance, filename):
	return os.path.join('photos', 'extras', filename)


def get_slug_name(obj_name):
	obj_name = str(obj_name).lower()
	obj_name = obj_name.replace('  ',' ')
	obj_name = obj_name.replace(' ','_')
	return obj_name

def get_item_slug_name(item):
	item_slug = 'shop/'+str(get_slug_name(item.category))+'/'+get_slug_name(item)
	return item_slug


class ItemCategory(models.Model):
	TYPE_CHOICES = (
			('0','others'),
			('1','cakes'),
			('2','gifts')
		)
	name = models.CharField(max_length=30)
	item_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='1')
	slug = models.SlugField(unique=True, editable=False)

	def __unicode__(self):
		return self.name

	#TODO fix this
	def get_total_cakes(self):
		all_cakes = Item.objects.filter(category=self)
		return len(all_cakes)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = get_slug_name(self.name)
		super(ItemCategory, self).save(*args,**kwargs)

class Item(models.Model):
	name = models.CharField(max_length=100, unique=True)
	old_price = models.FloatField(null=True,default=0)
	sale_price = models.FloatField()	
	category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
	brief_detail = models.TextField()
	image_file = models.ImageField(upload_to=get_image_upload_path, null=True)
	image_file_for_cart = ImageSpecField(source='image_file',processors=[ResizeToFill(100, 50)],
											format='JPEG',options={'quality': 60})
	image_file_for_carousel_and_gallery = ImageSpecField(source='image_file',processors=[ResizeToFill(200, 200)],
											format='JPEG',options={'quality': 60})
	in_stock = models.IntegerField(default=0)
	featured = models.BooleanField(default=False)
	show_as_new = models.BooleanField(default=False)
	slug = models.SlugField(unique=True, editable=False)
	date_added= models.DateTimeField(editable=False)


	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = get_slug_name(self)
			self.date_added = datetime.datetime.now()
		super(Item, self).save(*args,**kwargs)

	def admin_display_image(self):
		return u"<img src='/media/%s' width=70>" %self.image_file
	admin_display_image.allow_tags = True

	def add_to_cart(self,request):
		s_id = str(self.id)
		saved_list = request.session.get('cart_items')
		if not s_id in saved_list:
			saved_list.append(s_id)
			request.session['cart_items'] = saved_list
		return request
		

	def remove_from_cart(self,request):
		s_id = str(self.id)
		saved_list = request.session.get('cart_items')
		if s_id in saved_list:
			saved_list.remove(s_id)
			request.session['cart_items'] = saved_list
		return request
		

	def is_in_cart(self,request):
		saved_list = request.session.get('cart_items')
		if self.id in saved_list or str(self.id) in saved_list:
			return True
		return False

	def get_cart_image_url(self):
		try:
			return self.image_file_for_cart.url				
		except IOError as e:
			pass
		return self.image_file.url

	def get_gallery_carousel_image_url(self):
		try:
			return self.image_file_for_carousel_and_gallery.url
		except IOError as e:
			return self.image_file.url

	def get_full_item_detail_link(self,request):
		url = reverse('shop-item-detail-view', kwargs={'item_category':self.category.slug,'item_slug':self.slug})
		return request.build_absolute_uri(url)

	def get_relative_item_detail_link(self):
		return reverse('shop-item-detail-view', kwargs={'item_category':self.category.slug,'item_slug':self.slug})

	def get_extra_images(self):
		return ExtraImages.objects.filter(related_item=self)



class ExtraImages(models.Model):
	name = models.ImageField(upload_to=get_extra_images_upload_path, null=True)

	image_in_list = ImageSpecField(source='name',processors=[ResizeToFill(200,200)],
											format='JPEG',options={'quality': 60})
	related_item = models.ForeignKey(Item, on_delete=models.CASCADE)

	def get_image_url(self):
		pass



class GiftItems(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

