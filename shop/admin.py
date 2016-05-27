from django.contrib import admin
from . import models
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
	list_display = ('admin_display_image','name','old_price','sale_price','category','in_stock')

class ExtraImagesAdmin(admin.ModelAdmin):
	list_display = ('name','related_item')
		

admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemCategory)
admin.site.register(models.ExtraImages, ExtraImagesAdmin)