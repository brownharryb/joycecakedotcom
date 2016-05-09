from django.contrib import admin
from . import models
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
	list_display = ('admin_display_image','name','old_price','sale_price','category','in_stock')
		

admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemCategory)