import string

class CodeType:
	"""
	Select the type of code to be generated.
	---
	CodeType.digits - Numerical values only (0-9)\n
	CodeType.strings - String values only (a-zA-Z)\n
	CodeType.digits - String lower case values only (a-z)\n
	CodeType.digits - Punctuation marks only (!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~)\n
	"""
	testing = [string.digits, string.ascii_letters, string.ascii_lowercase, string.ascii_uppercase, string.punctuation]
	default = string.digits
	digits = string.digits
	strings = string.ascii_letters
	strings_lowercase = string.ascii_lowercase
	strings_uppercase = string.ascii_uppercase
	punctuation = string.punctuation

