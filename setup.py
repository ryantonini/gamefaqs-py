from distutils.core import setup

setup(
    name='GameFaqsPY',
    version='0.1.0',
    author='Ryan Tonini',
    packages=['gamefaqs'],
    url='https://github.com/ryantonini/gamefaqs-py',
    license='GPLv3 (see LICENSE)',
    description='Retrieve and manage game data from GameFAQS',
    long_description=open('README.rst').read(),
    package_data={'gamefaqs': ['dump.sql']},
    scripts=['gamefaqs/load_data.py']
)