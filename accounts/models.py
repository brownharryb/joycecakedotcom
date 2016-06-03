from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from shop import models as shopmodels
from mainsite import misc_functions
from django.core.urlresolvers import reverse
import datetime
from mainsite import misc_functions

NAME_LENGTH = 30
PASSWORD_LENGTH = 20
EMAIL_LENGTH = 20
MOBILE_NUMBER_LENGTH = 20
DELIVERY_FORM_INPUT_LENGTH = 100
TRANSACTION_ID_STRING_LENGTH = 30

class UserInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	mobile_phone = models.CharField(max_length=MOBILE_NUMBER_LENGTH)
	delivery_address1 = models.CharField(max_length=DELIVERY_FORM_INPUT_LENGTH,null=True)
	delivery_address2 = models.CharField(max_length=DELIVERY_FORM_INPUT_LENGTH,null=True,blank=True)
	city = models.CharField(max_length=DELIVERY_FORM_INPUT_LENGTH,null=True)
	state = models.CharField(max_length=DELIVERY_FORM_INPUT_LENGTH,null=True, default='Rivers')
	country=models.CharField(max_length=DELIVERY_FORM_INPUT_LENGTH,null=True, default='Nigeria')
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
	transaction_id_string = models.CharField(max_length=TRANSACTION_ID_STRING_LENGTH,editable=False,unique=True)
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
			self.transaction_id_string = misc_functions.generate_key(TRANSACTION_ID_STRING_LENGTH)
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

class BankAccountManager(models.Manager):

	def names_choices_tuple(self):
		cnt = 1
		
		returnVal = []
		all_objs = self.all()
		for i in all_objs:
			temp = []
			temp.append(cnt)
			extra_txt = i.account_number
			if i.name_on_account:
				extra_txt = '{0} -- {1}'.format(i.account_number,i.name_on_account)
			temp.append('{0} -- {1}'.format(i.bank_name,extra_txt))
			returnVal.append(tuple(temp))
			cnt+=1
		return tuple(returnVal)

class BankAccount(models.Model):
	TYPE_CHOICES = (
		('s','savings'),
		('c','current'),
		)
	bank_name = models.CharField(max_length=250)
	account_number = models.CharField(max_length=20)
	account_type = models.CharField(max_length=1,choices=TYPE_CHOICES, default='s')
	name_on_account = models.CharField(max_length=250,blank=True,null=True)
	objects = BankAccountManager()


	def __unicode__(self):
		return self.bank_name

	def get_all(self):
		return self.objects.all()

	def get_all_names_as_choice_tuple(self):
		cnt = 1
		temp = []
		returnVal = []
		all_objs = self.objects.all()
		for i in all_objs:
			temp.append(cnt)
			temp.append(i.bank_name)
			returnVal.append(tuple(temp))
			cnt+=1
		return tuple(returnVal)
	NAME_CHOICES = get_all_names_as_choice_tuple


