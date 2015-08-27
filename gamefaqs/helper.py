"""
Useful global variables and functions used by many modules.

Copyright (C) 2015  Ryan Tonini

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import requests
import urllib
import bs4

# URL of the homepage of the gamefaqs website
gamefaqsURL_base = "http://www.gamefaqs.com"

# http://www.gamefaqs.com/search/index.html?game=
gamefaqsURL_search_game = gamefaqsURL_base + "/search/index.html?game="

# http://www.gamefaqs.com/features/company/
gamefaqsURL_search_company = gamefaqsURL_base + "/features/company/?search="

# http://www.gamefaqs.com/features/topgames/
gamefaqsURL_top100 = gamefaqsURL_base + "/features/topgames/"

def get_bs4(url, parser="html.parser"):
    """Return a bs4 object for the webpage corresponding to the given url.
    
    The default parser is the 'html_parser'.
    """
    data = requests.get(url).text
    soup = bs4.BeautifulSoup(data, parser)
    return soup
    
def encode(value):
    """Return the url compatible (encoded) form of value."""
    encoded_value = urllib.quote_plus(value)
    return encoded_value   
    