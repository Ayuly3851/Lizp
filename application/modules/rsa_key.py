import os

def save_key(key, name):
	if not os.path.exists('keys/'):
		os.mkdir('keys')
	with open(f'keys/{name}.key', 'wb') as f:
		f.write(key.save_pkcs1())
	