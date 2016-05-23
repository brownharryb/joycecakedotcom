from django.contrib import admin
from . import models

class UserInfoAdmin(admin.ModelAdmin):
	list_display = ('user','mobile_phone','delivery_address1','delivery_address2','city','state','country','activation_key')

class UserTransactionAdmin(admin.ModelAdmin):
	list_display =('id','user','transaction_date','transaction_complete_date',
					'payment_medium','payment_confirmed','transaction_status')
		
		

admin.site.register(models.UserInfo, UserInfoAdmin)
admin.site.register(models.UserTransaction, UserTransactionAdmin)