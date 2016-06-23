from django.contrib import admin
from . import models

# Register your models here.
class SocialNetworkAdmin(admin.ModelAdmin):
	list_display = ('social_name','social_link','social_display')

class PersonalDetailAdmin(admin.ModelAdmin):
	list_display = ('name','option','display')

admin.site.register(models.SocialNetworks,SocialNetworkAdmin)
admin.site.register(models.PersonalDetail,PersonalDetailAdmin)