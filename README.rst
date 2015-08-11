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

    pip install GameFaqsPY

or installable via ``git clone`` and ``setup.py``

::

    git clone git@github.com:ryantonini/gamefaqs-py.git
    sudo python setup.py install

After installation, run the following python script in your project files directory:

::

    python load_data.py
    
Usage
-----
