GameFaqsPY
========

GameFaqsPY is a python package useful to retrieve and manage game data from the GameFAQS website.  The package is written in pure python and provides the following game information:

* Title
* Description
* Platform
* Release Date
* Companies
* ESRB Rating
* Metascore
* User Rating (/5)
* Difficulty
* Length (hr)

Installation
------------

GameFaqsPY is conveniently available via pip:

::

    pip install gamefaqs-py

or installable via ``git clone`` and ``setup.py``

::

    git clone git@github.com:ryantonini/gamefaqs-py.git
    sudo python setup.py install

After installation, run the following python script in your project files directory:

::

    python load_data.py
    
The script will create a SQLite database file in the current working directory loaded with data from http://www.gamefaqs.com/.

Usage
-----

A code example:

.. code:: python

    from gamefaqs import access
    gf_access = access.GameFaqs()
    
    peace_walker = gf_access.searchGame("Metal Gear Solid: Peace Walker")[0]
    print peace_walker
    
    for game in gf_access.searchByCompany("Akella"):
        print game["title"], game["platform"], game["release_date"]

License
-------

GNU General Public License Version 3.  See LICENSE for more details.
    
