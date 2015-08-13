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

After installation, execute the ``run_load.py`` script via: 

::

    python {FILE_PATH}/run_load.py
    
The script will create a SQLite database file in the current working directory containing data loaded from http://www.gamefaqs.com/.  The ``{FILE_PATH}`` is the PATHNAME to the location of the ``run_load.py`` file on your computers file system.   

If your working in a UNIX environment, you can find the file PATH via:

::

    mdfind "run_load.py"
    
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
    
