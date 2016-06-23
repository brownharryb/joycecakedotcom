from __future__ import unicode_literals

from django.db import models

class SocialNetworks(models.Model):
	social_name = models.CharField(max_length=30)
	social_link = models.CharField(max_length=250)
	social_display = models.BooleanField()

	def __unicode__(self):
		return self.social_name

	def should_display(self):
		return self.social_display


class PersonalDetail(models.Model):
	name = models.CharField(max_length=250)
	option = models.CharField(max_length=250)
	display = models.BooleanField()

	def __unicode__(self):
		return self.name

	def should_display(self):
		return self.display



