from django.core.exceptions import ValidationError



def validate_field(text_to_validate,allowed,field_name):
 	for i in text_to_validate:
		if not i in allowed:
			raise ValidationError('Invalid '+str(field_name))


def validate_username(username):
	allowed = 'abcdefghijklmnopqrstuvwxyz0123456789_'
	validate_field(username,allowed,'Username')

def validate_password(password):
	allowed = 'abcdefghijklmnopqrstuvwxyz0123456789'
	validate_field(password,allowed,'Password')

def validate_mobile_numbers(mobile_number):
	allowed = '0123456789+-'
	validate_field(mobile_number,allowed,'Mobile Number')

