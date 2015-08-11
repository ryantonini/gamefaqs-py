from distutils.core import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='gamefaqs-py',
    version='0.1.1',
    author='Ryan Tonini',
    author_email ='ryantonini@yahoo.com',
    packages=['gamefaqs'],
    url='https://github.com/ryantonini/gamefaqs-py',
    license='GPLv3 (see LICENSE)',
    description='Retrieve and manage game data from GameFAQS.',
    long_description=long_description,
    package_data={'gamefaqs': ['data/dump.sql']},
    scripts=['gamefaqs/scripts/load_data.py']
)
