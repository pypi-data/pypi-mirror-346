import random
from xtools.cache import Cache
from .type import CodeType

class SafeCode:
	_configured = False
	_len_code = None
	_cache = None
	_code_type = None
	_debug_mode = False

	@classmethod
	def configure(cls, len_code: int = 4, ttl: int = 120, max_size: int = 1024, code_type: CodeType | list[CodeType] = CodeType.default, debug_mode: bool = False):
		"""
		Initialises the cache with the specified parameters.

		:param len_code: fixed length of generated code (default 4 digits).
		:param ttl: Time to Live (TTL) for each item in the cache in seconds (default is 120 seconds).
		:param code_type: Select the type of code to be generated.
		:param max_size: Maximum cache size (default is 1024 items).
		:param debug_mode: Debug mode for developers (default is False).
		"""
		cls._len_code = len_code
		cls._cache = Cache(ttl, max_size)
		cls._code_type = [_type for _type in code_type]
		cls._debug_mode = debug_mode
		cls._configured = True

		if cls._debug_mode:
			print("[DEGUB] The configuration has been successfully set up")

	@classmethod
	def _check_configured(cls):
		if not cls._configured:
			raise RuntimeError("SafeCode is not configured. Call SafeCode.configure(...) first.")

	@classmethod
	def genCode(cls) -> str:
		"generates random code without using memory."
		cls._check_configured()
		if cls._debug_mode:
			print("[DEGUB] genCode() -> The random code was successfully generated.")

		strings = ''.join(cls._code_type)
		return str(''.join(random.choices(strings, k=cls._len_code)))

	@classmethod
	def newCode(cls) -> str:
		"generates a unique code using memory."
		cls._check_configured()
		if cls._debug_mode:
			print("[DEGUB] newCode() -> The creation of a unique code is performed...")
		while True:
			code = cls.genCode()
			if not cls._cache.get(code):
				if cls._debug_mode:
					print("[DEGUB] newCode() -> The unique code was successfully created.")
				cls._cache.set(code, True)
				if cls._debug_mode:
					print("[DEGUB] newCode() -> The unique code was successfully stored in memory.")
				return code
			else:
				if cls._debug_mode:
					print(f"[DEBUG] newCode() -> We found a match for code `{code}` overgeneration.")

	@classmethod
	def checkCode(cls, code: str) -> bool:
		"""Checks the code for uniqueness.\n
		:return: True - The code is available in memory
		:return: False - The code is not available in memory"""
		cls._check_configured()
		if bool(cls._cache.get(code)):
			return True
		return False