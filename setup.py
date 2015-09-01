from distutils.core import setup
 
LONG_DESCRIPTION = open('README.rst').read()

keywords = ["game", "company", "cheats", "web", "http", "database", 
            "scraper", "data", "api", "package"]
setup(
    name='gamefaqs-py',
    version='0.2.5',
    author='Ryan Tonini',
    author_email ='ryantonini@yahoo.com',
    packages=['gamefaqs'],
    url='https://github.com/ryantonini/gamefaqs-py',
    license='GNU General Public License v3.0',
    description='Retrieve and manage game data from GameFAQS.',
    long_description=LONG_DESCRIPTION,
    keywords=keywords,
    package_data={'gamefaqs': ['data/gamefaqs.sql']},
    scripts=['scripts/run_load.py'],
    install_requires=['BeautifulSoup==3.2.1', 'requests==2.7.0'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Games/Entertainment",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development"]
)
