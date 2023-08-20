import re
import string
import random

class Password:

	def __init__(self):
		self.characters = string.ascii_letters + string.digits + string.punctuation

	# def check_password_security(self, password: str) -> int:

	def generate_password(self, size: int) -> str:
		password = ""
		for i in range(size):
			password += random.choice(self.characters)

		return password