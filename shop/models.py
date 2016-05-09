from __future__ import unicode_literals

from django.db import models
import os, datetime


def get_image_upload_path(instance, filename):
	cat = str(instance.category)
	cat = cat.replace(' ','_').lower()
	return os.path.join('photos', cat, filename)


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
		return 20

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



class GiftItems(models.Model):
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name

