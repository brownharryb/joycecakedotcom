from django.contrib import admin
from . import models

# Register your models here.
class SocialNetworkAdmin(admin.ModelAdmin):
	list_display = ('social_name','social_link','social_display')

admin.site.register(models.SocialNetworks,SocialNetworkAdmin)