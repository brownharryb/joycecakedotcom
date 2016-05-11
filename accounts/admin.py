from django.contrib import admin
from . import models

class UserInfoAdmin(admin.ModelAdmin):
	list_display = ('user','mobile_phone','delivery_address1','delivery_address2','city','state','country','activation_key')
		

admin.site.register(models.UserInfo, UserInfoAdmin)