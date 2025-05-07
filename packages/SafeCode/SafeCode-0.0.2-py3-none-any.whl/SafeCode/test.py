

from .type import CodeType
from .safecode import SafeCode


class CodeTest:
	"""To check if the code works."""
	@staticmethod
	def test_memory_work(loop_count: int = 10, stop_failed: bool = False):
		"""Memory performance check. Checking if the code is stored and if this value is retrieved.

		:param loop_count: Number of test cycles.
		:param stop_failed: Stop the cycle if a failed is detected.
		"""
		is_failed = False
		for code_type in CodeType.testing:
			print(f"Check CodeType is {code_type}")
			SafeCode.configure(code_type=code_type)
			for i in range(loop_count):
				code = SafeCode.newCode()
				print(SafeCode.checkCode(code))
				if SafeCode.checkCode(code):
					print(f"[V] The code is unique. Cycle {i} worked correctly.")
				else:
					is_failed = True
					print(f"[X] The code is non-unique. Cycle {i} failed!")
					if stop_failed:
						print("[X] The cycle has been stopped.")
					break
			if is_failed:
				print("[X] The main cycle has been stopped.")
				break

