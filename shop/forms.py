from django import forms
from django.contrib.auth.models import User
from accounts.models import UserInfo, BankAccount
from mainsite import misc_functions
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from accounts import models as accountsmodels


TRANSACTION_ID_LENGTH = 30
class CheckoutContactForm(forms.Form):
	fullname = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder':'Name'}))
	mobile = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Mobile Number'}))


class AlreadyPaidForm(forms.Form):
	NAME_CHOICES = BankAccount.objects.names_choices_tuple()
	bank_name = forms.ChoiceField(widget=forms.Select, choices=NAME_CHOICES)
	amount_paid = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'placeholder':'Amount Paid(Numbers only)'}))
	transaction_id = forms.CharField(max_length=TRANSACTION_ID_LENGTH,widget=forms.TextInput(attrs={'placeholder':'Transaction ID'}))
	customer_name = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Name'}))
	customer_mobile = forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder':'Mobile Number'}))
	extra_info = forms.CharField(max_length=250,required=False,widget=forms.Textarea(attrs={'placeholder':'Extra Information','rows':1}))


	def get_bank_details(self):
		returnData = 'Bank'
		for i in self.NAME_CHOICES:
			if str(i[0])== str(self.cleaned_data['bank_name']):
				returnData = i[1]
		return returnData


	def clean(self):
		super(AlreadyPaidForm,self).clean()
		temp = {}
		temp['Bank Information'] = bank_info_selected = self.cleaned_data.get('bank_name')
		temp['Amount Paid'] = amount_paid = self.cleaned_data.get('amount_paid')
		temp['Transaction Id'] = transaction_id = self.cleaned_data.get('transaction_id')
		temp['Name'] = customer_name = self.cleaned_data.get('customer_name')
		temp['Mobile Number'] = customer_mobile = self.cleaned_data.get('customer_mobile')
		

		emptychar = misc_functions.input_is_not_empty(temp)
		if not emptychar == 1:
			raise ValidationError('%s is required!' %emptychar)
		temp['extra_info'] = extra_info = self.cleaned_data.get('extra_info')

		if not misc_functions.input_is_only_numbers(amount_paid):
			raise ValidationError('Inalid Amount!')

		if not misc_functions.mobile_number_is_ok(customer_mobile):
			raise ValidationError('Invalid Mobile Number!')

		if len(transaction_id)<TRANSACTION_ID_LENGTH:
			raise ValidationError('Please check your transaction id!')

		if not misc_functions.input_is_alpha_numerals({'Transaction id':transaction_id}):
			raise ValidationError('Please check your transaction id!')

		if not misc_functions.input_is_alpha_numerals({'Name':customer_name}):
			raise ValidationError('Invalid Name!')

		if not misc_functions.input_is_alpha_numerals({'Extra Info':extra_info}):
			raise ValidationError('Please check your Extra Information input!!')
		try:
			user_transaction = accountsmodels.UserTransaction.objects.get(transaction_id_string=transaction_id)
			total_price = user_transaction.get_total_price()
			print 'inputed={0} transaction={1}'.format(amount_paid,total_price)
			if not float(total_price)==float(amount_paid):
				raise ValidationError('Inputed price and transaction price don\'t match!!')
		except ObjectDoesNotExist as e:
			raise ValidationError('Invalid Transaction Id')



		return self.cleaned_data


		