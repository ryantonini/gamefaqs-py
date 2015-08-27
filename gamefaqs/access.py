"""
Access to GameFaqs web server to search game/company info.

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

import helper
import company
import game
import info

# specifies the category of games returned from search
search_matches = ["Best Matches"]
   
def GameFaqs(access_system="http"):
    """Return an instance of the appropriate class.
    
    The 'access_system' keyword argument must be a string representing the type
    of data access you want to use.  There are different systems to access
    gamefaqs data: fetch data from the web server directly or fetch from the
    online mysql database.
    
    Supported access systems: (default) "http" and "sql".
    
    NOTE: The "sql" access system has yet to implemmented.
    """
    if access_system == "sql":
        gf_access = GameFaqsDB()
    elif access_system == "http":
        gf_access = GameFaqsBase()
    return gf_access


class GameFaqsBase(object):
    """The class used to search for a Game/Company and get a Game/Company 
    object using http/web."""

    def __init__(self):
        """Initialize the parser"""
        self.fetch = info.FetchInfo()
        
    def search_game(self, title):
        """Return a list of Game objects for a query for the given title."""
        all_games = []
        encoded_title = helper.encode(title)
        # full game search url
        url = helper.gamefaqsURL_search_game + encoded_title
        soup = helper.get_bs4(url)
        tags = soup.find_all("div", {"class": "pod"})
        for tag in tags:
            criteria_tag = tag.find("h2")
            # only include games under best matches category
            if criteria_tag and criteria_tag.text in search_matches:
                best_matches = tag.find_all("tr")
                for match in best_matches:
                    # get game platform
                    p = match.find("td", {"class": "rmain"}).text
                    platform = p.replace(" ", "").replace("\r\n", "")
                    info = match.find("td", {"class": "rtitle"})
                    # get game url
                    game_url = helper.gamefaqsURL_base + info.contents[1]["href"]
                    # get game title
                    game_title = info.text.replace("\n", "")
                    obj = game.Game(game_url, dict(title=game_title,
                                                    platform=platform))                                           
                    all_games.append(obj)
                break
        return all_games
        
    def search_company(self, name, limit=40):
        """Returns a list of Company objects for a query for the given name.
        
        The maximum number of companies to be returned is set by limit.
        """
        companies = []
        encoded_name = helper.encode(name)
        # full company search url
        url =  helper.gamefaqsURL_search_company + encoded_name
        soup = helper.get_bs4(url)
        company_tags = soup.find_all("table")[1].find_all("a")
        count = 0
        for tag in company_tags:
            companies.append(company.Company(helper.gamefaqsURL_base + tag["href"],
                                             dict(name=tag.text)))
            count += 1
            if (count >= limit):
                break
        return companies
        
    def update(self, gc, info=["general"], override=False):
        """Given a Game/Company object with only partial information, retrieve 
        the required set of information.
        
        Info is the list of sets of information to retrieve.  To view valid 
        information sets see the all_info instance variable.  The default info 
        set is general.  NOTE: The keys of the main info set cannot be updated.
        
        If override is set, the info is retrieved and updated even if its 
        already in the object.
        """
        results = {}
        new_info = []
        self.fetch.save(gc.url)
        for i in info:
            if gc.has_current_info(i) and not override:
                continue
            new_info.append(i)
        if isinstance(gc, game.Game):   
            if new_info:        
                results = self.fetch.find_game_keys(new_info)
            else:
                return 
        elif isinstance(gc, company.Company):
            if new_info:
                results = self.fetch.find_company_keys(new_info)
            else:
                return 
        items = results.keys()
        for infoset in new_info:
            keys = gc.get_infoset_keys(infoset)
            for key in keys:
                # key requested was not found, so set to None
                if key not in items:
                    results[key] = None
            # add new info set to current list
            gc.add_to_current_info(infoset)    
        gc.set_data(results)     
        self.fetch.remove()
    
    def get_top100_games(self):
        """Return the list of the top 100 most popular games today."""
        games_list = []
        soup = helper.get_bs4(helper.gamefaqsURL_top100)
        items = soup.find("tbody").find_all("tr")
        for elem in items:
            tag = elem.find("a")
            url = helper.gamefaqsURL_base + tag["href"]
            title = tag.text
            platform = elem.find_all("td")[4].text
            games_list.append(game.Game(url, dict(title=title, 
                                                  platform=platform)))
        return games_list
            
            
class GameFaqsDB(object):
    """The class is used to search for a Game/Company and get a Game/Company 
    object using mysql database."""
    #YET TO BE IMPLEMENTED
    pass
    
    
    
        
    