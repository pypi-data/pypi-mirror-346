# SafeCode
[?] A simple library for generating unique codes. Suitable if you want to generate unique codes and send them by sms to confirm your phone number, mail or other industry.

## Installation

[Python](https://python.org) require 3.6+

install SafeCode libary:
```sh
pip install SafeCode
```

## Examples
### Configuration setting
```python
from SafeCode import SafeCode as SF
from SafeCode import CodeType

SF.configure(len_code: int = 4, ttl: int = 120, max_size: int = 1024, code_type: CodeType | list[CodeType] = CodeType.default, debug_mode: bool = False)

"""
[!] The configuration is set up once when the whole project is started. [!]

Initialises the cache with the specified parameters.

:param len_code: fixed length of generated code (default 4 digits).
:param ttl: Time to Live (TTL) for each item in the cache in seconds (default is 120 seconds).
:param code_type: Select the type of code to be generated.
:param max_size: Maximum cache size (default is 1024 items).
:param debug_mode: Debug mode for developers (default is False).
"""
```
### Generation of a unique code
```python
from SafeCode import SafeCode as SF
from SafeCode import CodeType

SF.configure(len_code = 6, ttl = 240, code_type = [CodeType.digits, CodeType.strings_uppercase])

unique_code = SF.newCode()

"""
The `newCode()` function returns a unique code. 
The code is generated and checked for uniqueness, if this code is already in memory, it is re-generated.

always returns a string
"""
```
### Random code generation
```python
from SafeCode import SafeCode as SF
from SafeCode import CodeType

SF.configure(len_code = 6, ttl = 240, code_type = [CodeType.digits, CodeType.strings_uppercase])

random_code = SF.genCode()

"""
The `genCode()` function returns a random code. 
This code is not stored in memory and memory is not used during generation, so it may have already been encountered earlier or later.

always returns a string
"""
```
### Uniqueness check
```python
from SafeCode import SafeCode as SF
from SafeCode import CodeType

SF.configure(len_code = 6, ttl = 240, code_type = [CodeType.digits, CodeType.strings_uppercase])

random_code = SF.genCode()

if SF.checkCode(random_code):
	return "The code is available in memory. It's non-unique."
else:
	return "The code is not available in memory. It's unique."

"""
The `checkCode()` function checks the code for its presence in memory
When using the `newCode()` function, this procedure of checking the code for uniqueness is not required, only for the `genCode()` function

always returns a bool
"""
```

#### Documentation for the library: [GitHub WIKI](https://github.com/SikWeet/SafeCode/wiki)

##the library will be constantly updated and will be better soon!
