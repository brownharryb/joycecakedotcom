from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from shop import models as shopmodels
from mainsite import misc_functions
from django.core.urlresolvers import reverse
import datetime
from mainsite import misc_functions


class UserInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	mobile_phone = models.CharField(max_length=20)
	delivery_address1 = models.CharField(max_length=100,null=True)
	delivery_address2 = models.CharField(max_length=100,null=True,blank=True)
	city = models.CharField(max_length=20,null=True)
	state = models.CharField(max_length=30,null=True, default='Rivers')
	country=models.CharField(max_length=30,null=True, default='Nigeria')
	activation_key = models.CharField(max_length=30, editable=False, null=True)
	recovery_key = models.CharField(max_length=40, editable=False, null=True)

	def __unicode__(self):
		return self.mobile_phone

	def save(self, *args, **kwargs):
		if not self.id:
			self.activation_key = misc_functions.generate_key(30)
		super(UserInfo, self).save(*args,**kwargs)

	def save_recovery_key(self):
		self.recovery_key =  misc_functions.generate_key(40)
		self.save()

	def get_recovery_link(self,request):
		if not self.recovery_key:
			self.save_recovery_key
		url = request.build_absolute_uri(reverse('recover_password', kwargs={'username':self.user.username,'recovery_key':self.recovery_key}))
		return url



class UserTransaction(models.Model):
	TRANSACTION_STATUS_CHOICES=(
			('0','pending'),
			('1','complete'),
			('2','others')
		)
	PAYMENT_MEDIUM_CHOICES = (
			('0','cash on delivery'),
			('1','interswitch'),
			('2','paypal')
		)
	user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
	transaction_id_string = models.CharField(max_length=20,editable=False,unique=True)
	transaction_date = models.DateTimeField(editable=False)
	transaction_complete_date = models.DateTimeField(null=True,blank=True)
	items = models.ManyToManyField(shopmodels.Item)
	payment_medium = models.CharField(max_length=1,default='0',choices=PAYMENT_MEDIUM_CHOICES)
	payment_confirmed = models.BooleanField(default=False)
	transaction_status = models.CharField(max_length=1, choices=TRANSACTION_STATUS_CHOICES, default='0')
	session_string = models.TextField(blank=True,editable=False)



	def save(self, *args, **kwargs):
		if not self.id:
			self.transaction_date = datetime.datetime.now()
			self.transaction_id_string = misc_functions.generate_key(30)
		super(UserTransaction, self).save(*args,**kwargs)


	def get_total_item_details(self):
		data_list = misc_functions.decode_session_string(self.session_string)

		for i in data_list:
			i['item_id'] = shopmodels.Item.objects.get(pk=int(i['item_id']))
		return data_list

	def get_total_price(self):
		totalprice = 0
		data = self.get_total_item_details()
		for i in data:
			totalprice +=float(i['item_full_price'])
		return totalprice


