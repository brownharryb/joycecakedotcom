import random



def generate_key(length):
	return_data = []
	data = 'abcdefghijklmnopqrstuvwxyz0123456789'
	for i in xrange(length):
		return_data.append(random.choice(data))
	return_data = ''.join(return_data)
	return return_data

def input_is_alpha_numerals(input_dict, space_allowed=False):
	allowed = 'abcdefghijklmnopqrstuvwxyz0123456789_-'
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



