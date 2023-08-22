import re
import string
import random

class Password:

	def __init__(self):
		pass

	# def check_password_security(self, password: str) -> int:

	def generate_password(self, length: int = 20, 
						have_ascii_lowercase: bool = True,
						have_ascii_uppercase: bool = True,
						have_digits: bool = True,
						have_punctuation: bool = True,
						punctuation_characters: str = string.punctuation
						) -> str:

		password = ""
		self.characters = ""

		if have_ascii_lowercase:
			self.characters += string.ascii_lowercase
		if  have_ascii_uppercase:
			self.characters += string.ascii_uppercase
		if have_digits:
			self.characters += string.digits
		if have_punctuation:
			self.characters += punctuation_characters

		if self.characters == '':
			return ''

		for i in range(length):
			password += random.choice(self.characters)

		return password