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

    git clone https://github.com/ryantonini/gamefaqs-py
    sudo python setup.py install

After installation, you will have to run the `run_load.py` script.  The script will create a SQLite database file in the current working directory loaded with data from http://www.gamefaqs.com/.  

If your working in a UNIX environment, you can find the PATH via:

::

    mdfind "run_load.py"
    
If your working in a Virtual Environment, then you can run the script via:

::
    
    python ./venv/bin/run_load.py

Usage
-----

A code example:

.. code:: python

    from gamefaqs import access
    gf_access = access.GameFaqs()
    
    peace_walker = gf_access.searchGame("Metal Gear Solid: Peace Walker")[0]
    print peace_walker
    
    for game in gf_access.searchByCompany("Akella"):
        print game.data["title"], game.data["platform"], game.data["release_date"]

License
-------

GNU General Public License Version 3.  See LICENSE for more details.
    
