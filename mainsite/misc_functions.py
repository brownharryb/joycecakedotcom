import random



def generate_key(length):
	return_data = []
	data = 'abcdefghijklmnopqrstuvwxyz0123456789'
	for i in xrange(length):
		return_data.append(random.choice(data))
	return_data = ''.join(return_data)
	return return_data



