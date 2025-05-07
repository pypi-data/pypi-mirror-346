from setuptools import setup, find_packages

def readme():
	with open('README.md', 'r') as f:
		return f.read()


setup(
	name='SafeCode',
	version='0.0.1',
	author='Xpeawey',
	author_email='girectx@gmail.com',
	description='A simple library for generating unique codes. Suitable if you want to generate unique codes and send them by sms to confirm your phone number, mail or other industry.',
	long_description=readme(),
	long_description_content_type='text/markdown',
	url='https://github.com/SikWeet/SafeCode/tree/main',
	packages=find_packages(),
	classifiers=[
		'Programming Language :: Python :: 3.11',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent'
	],
	keywords=['safecode', 'safe code', 'code', 'pypi safecode', 'pypi safe code', 'pypi lib generation code', 'python generation code'],
	install_requires=['xtools-py>=0.1.1'],
	project_urls={
		'GitHub': 'https://github.com/SikWeet'
	},
	python_requires='>=3.6'
)