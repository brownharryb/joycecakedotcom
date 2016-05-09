from django.shortcuts import render
from . import models
import random


#********************************Gallery*****************
def gallery_view(requests):
	try:
		cat = models.ItemCategory.objects.get(pk=1)
		cakes = models.Item.objects.filter(category=cat)
		cakes = list(cakes)
		cakes = randomize_list(cakes)
		return render(requests,'gallery.html',{'cakes':cakes})
	except:
		return render(requests,'page404.html')

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
