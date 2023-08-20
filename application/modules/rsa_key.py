def save_key(key, name):
	with open(f'keys/{name}.key', 'wb') as f:
		f.write(key.save_pkcs1())
	