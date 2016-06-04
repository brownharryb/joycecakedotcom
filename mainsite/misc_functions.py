import random
from datetime import datetime, timedelta
from django.http import  HttpRequest
from django.conf import settings
from django.core.mail import send_mail



def generate_key(length):
	return_data = []
	data = 'abcdefghijklmnopqrstuvwxyz0123456789'
	for i in xrange(length):
		return_data.append(random.choice(data))
	return_data = ''.join(return_data)
	return return_data

def input_is_alpha_numerals(input_dict, space_allowed=False):
	allowed = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-'
	if space_allowed:
		allowed +=' '
	for key in input_dict.keys():
		for j in input_dict[key]:
			if not j.lower() in allowed:
				return key
	return 1

def input_is_not_empty(input_dict):
	for key in input_dict.keys():
		if not input_dict[key]:
			return key
		val = ' '.join(input_dict[key].split())
		if val == '':
			return key
	return 1

def email_is_ok(email):
	allowed = 'abcdefghijklmnopqrstuvwxyz0123456789_-@.'
	for i in email:
		if not i.lower() in allowed:
				return False
	return True
def mobile_number_is_ok(mobile_number):
	allowed = '0123456789+-'
	for i in mobile_number:
		if not i in allowed:
			return False
	return True

def input_is_only_numbers(input_txt):
	allowed = '0123456789'
	for i in input_txt:
		if not i in allowed:
			return False
	return True

def get_seconds_time_value(time_type='seconds',number=None):
	if time_type == 'years':
		return number * 365 * 86400
	elif time_type == 'months':
		# average month days is 30
		return number * 30 * 86400
	elif time_type == 'days':
		return number * 86400
	elif time_type == 'hours':
		return number * 3600
	elif time_type == 'minutes':
		return number * 60		
	else:
		return number

def get_end_date_from_today(seconds):
	today = datetime.datetime.now()
	end_date = today + timedelta(seconds=seconds)
	return end_date
	
def randomize_list(list_obj):
	new_list = []
	while not list_obj == []:
		rdm = random.choice(list_obj)
		new_list.append(rdm)
		list_obj.remove(rdm)
	return new_list

# TODO ADD THIS TO ALL VIEWS
def confirm_sessions(request):
	cart_items = ''
	try:
		cart_items = request.session['cart_items']
	except KeyError:
		request.session['cart_items'] = []
	


def confirm_cookies(request):
	pass


def confirm_sessions_and_cookies(func):
	def inner(*args,**kwargs):
		request = ''
		for i in args:
			if isinstance(i,HttpRequest):
				request = i
		confirm_sessions(request)
		confirm_cookies(request)
		return func(*args,**kwargs)
	return inner


# TODO FIX THIS TO GET PROPER FULLNAME
def get_proper_fullname(fullname):
	return fullname

# TODO CREATE EMAIL BACKEND TO SEND EMAIL
def send_email(subject,recipients_list,msg):
	# try:
	send_mail(subject, msg, 'bomsy1@gmail.com',recipients_list, 
			fail_silently=False)
	# except:
	# 	return False
	return True

def decode_session_string(session_str):
	returnlist = []
	"item_session_string = _i3|q1|p5000.0_i2|q1|p4000.0_i5|q1|p4000.0_i4|q1|p5000.0"
	s = session_str.split('_')
	for i in s:
		if not i == '':
			e = i.split('|')
			tempdict={}
			for j in e:
				if j[0]=='i':
					tempdict['item_id'] = j[1:]
				if j[0]=='q':
					tempdict['item_qty'] = j[1:]
				if j[0]=='p':
					tempdict['item_full_price'] = j[1:]
			returnlist.append(tempdict)
	return returnlist

