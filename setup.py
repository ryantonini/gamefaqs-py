from distutils.core import setup
 
LONG_DESCRIPTION = open('README.rst').read()

setup(
    name='gamefaqs-py',
    version='0.2.3',
    author='Ryan Tonini',
    author_email ='ryantonini@yahoo.com',
    packages=['gamefaqs'],
    url='https://github.com/ryantonini/gamefaqs-py',
    license=' GNU General Public License v3.0',
    description='Retrieve and manage game data from GameFAQS.',
    long_description=LONG_DESCRIPTION,
    package_data={'gamefaqs': ['data/*.sql']},
    scripts=['scripts/run_load.py']
)
