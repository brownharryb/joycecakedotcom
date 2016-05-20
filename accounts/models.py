from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from shop import models as shopmodels
from mainsite import misc_functions
import datetime


class UserInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	mobile_phone = models.CharField(max_length=20)
	delivery_address1 = models.CharField(max_length=100,null=True)
	delivery_address2 = models.CharField(max_length=100,null=True,blank=True)
	city = models.CharField(max_length=20,null=True)
	state = models.CharField(max_length=30,null=True, default='Rivers')
	country=models.CharField(max_length=30,null=True, default='Nigeria')
	activation_key = models.CharField(max_length=30, editable=False, null=True)

	def __unicode__(self):
		return self.mobile_phone

	def save(self, *args, **kwargs):
		if not self.id:
			self.activation_key = misc_functions.generate_key(30)
		super(UserInfo, self).save(*args,**kwargs)


class UserTransaction(models.Model):
	TRANSACTION_STATUS_CHOICES=(
			('0','pending'),
			('1','complete'),
			('2','others')
		)
	PAYMENT_MEDIUM_CHOICES = (
			('0','cash_on_delivery'),
			('1','interswitch'),
			('2','paypal')
		)
	user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, null=True)
	mobile_phone = models.CharField(max_length=20)
	full_name = models.CharField(max_length=100)
	transaction_id_string = models.CharField(max_length=20,editable=False,unique=True)
	transaction_date = models.DateTimeField(editable=False)
	transaction_complete_date = models.DateTimeField(null=True,editable=False)
	items = models.ManyToManyField(shopmodels.Item)
	payment_medium = models.CharField(max_length=1,default=0)
	payment_confirmed = models.BooleanField(default=False)
	transaction_status = models.CharField(max_length=1, choices=TRANSACTION_STATUS_CHOICES, default='0')



	def save(self, *args, **kwargs):
		if not self.id:
			self.transaction_date = datetime.datetime.now()
			self.transaction_id_string = misc_functions.generate_key(30)
		super(UserTransaction, self).save(*args,**kwargs)