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
import sqlite3

import helper
import company
import game
import info
import cheats

# specifies the category of games returned from search
search_matches = ["Best Matches"]
   
def GameFaqs(access_system="http"):
    """Return an instance of the appropriate class.
    
    The 'access_system' keyword argument must be a string representing the type
    of data access you want to use.  There are different systems to access
    gamefaqs data: fetch data from the web server directly or reference a local 
    sqlite database file.
    
    Supported access systems: (default) "http" and "sql".
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
            
            
class GameFaqsDB(GameFaqsBase):
    """The class is used to search for a Game/Company and get a Game/Company 
    object using a sqlite database.  If the data is not found in the sqlite 
    database file, it is obtained via http/web server."""
    
    def __init__(self):
        """Connect to the db."""
        super(GameFaqsDB, self).__init__()
        self.db = sqlite3.connect("gamefaqs.db")
        self.cursor = self.db.cursor()
    
    def _insert(self, game):
        """Add game object to database."""
        try:
            # execute sql commands
            self.cursor.execute("""INSERT INTO INFO(title, description, platform,  
                                platform_long, release_date, esrb, url) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                                (game["title"], game["description"], game["platform"], 
                                 game["platform_long"], game["release_date"], 
                                    game["esrb"], game.url))
            # get gID
            game_id = self.cursor.lastrowid
            self.cursor.execute("""INSERT INTO RATING(gID, metascore, user_rating,
                                difficulty, length) VALUES (?, ?, ?, ?, ?)""",
                              (game_id, game["metascore"], game["user_rating"], 
                               game["difficulty"], game["length"]))
            for code in game["codes"]:    
                self.cursor.execute("""INSERT INTO CODES(gID, effect, code)
                                  VALUES (?, ?, ?)""", (game_id, code.effect, code.code))
            for unlockable in game["unlockables"]:
                self.cursor.execute("""INSERT INTO UNLOCKABLES(gID, unlockable, howto)
                                  VALUES (?, ?, ?)""", (game_id, unlockable.unlockable, 
                                                        unlockable.how_to))
            for co in game['companies']:
                self.cursor.execute("""INSERT INTO COMPANY(company_name, url)
                                    VALUES (?, ?)""", (co["name"], co.url))
                # get cID
                company_id = self.cursor.lastrowid
                self.cursor.execute("""INSERT INTO LINK(gID, cID) VALUES (?, ?)""",
                                     (game_id, company_id))   
            # commit changes in the database (either commit all or none)
            self.db.commit()
        except Exception, e:
            # for debugging
            print "Database Upload Failed. Game: ", game
            print str(e)
            # rollback in case of an error
            self.db.rollback()
    
    def search_game(self, title, override_db=False):
        """Check local database for game.  If not found, get from web server.
        
        If override_db is False (default), then a database search is performed, 
        followed by a web based search (if the database search produced no 
        matches).  If override_db is True, then a web based search is performed
        in place of the database search.
        """
        games_list = []
        if not override_db:
            self.cursor.execute("SELECT * FROM Info WHERE title = ?", (title,))
            while True:
                row = self.cursor.fetchone()
                if row == None:
                    break
                g = game.Game(row[7], dict(title=row[1], platform=row[3]),
                              objID=row[0])
                games_list.append(g)
        if games_list:
            return games_list
        if not games_list or override_db:
            games_list = super(GameFaqsDB, self).search_game(title)
            return games_list
    
    def search_company(self, name, override_db=False):
        """Check local database for company.  If not found, get from web 
        server.
        
        If override_db is False (default), then a database search is performed, 
        followed by a web based search (if the database search produced no 
        matches).  If override_db is True, then a web based search is performed
        in place of the database search.
        """
        company_list = []
        if not override_db:
            self.cursor.execute("SELECT * FROM Company WHERE company_name = ?", (name,))
            while True:
                row = self.cursor.fetchone()
                if row == None:
                    break
                c = company.Company(row[2], dict(name=row[1]), objID=row[0])
                company_list.append(c)
        if company_list:
            return company_list
        if not company_list or override_db:
            company_list = super(GameFaqsDB, self).search_company(name)
            return company_list
    
    def update(self, gc, info=["general"]):
        """Given a Game/Company object with only partial information, retrieve 
        the required set of information.  
        
        If the game object was not obtained via the database, then game object 
        will be updated via the web server.
        """
        idv = gc.get_id()
        if idv:
            # then game was obtained from database
            if isinstance(gc, game.Game):
                if "general" in info:
                    self.cursor.execute("""SELECT * FROM Info, Company WHERE gID = ? 
                                and cID in (SELECT cID FROM Link WHERE gID = ?)""", 
                                    (idv, idv))
                    first = True
                    companies = []
                    while True:
                        row = self.cursor.fetchone()
                        if row == None:
                            break
                        if first: 
                            general = dict(description=row[2], platform_long=row[4],
                                   release_data=row[5], esrb=row[6])
                            first = False
                        companies.append(company.Company(url=row[10], data=dict(name=row[9])))
                    general["companies"] = companies
                    gc.set_data(general)
                if "rating" in info:
                    self.cursor.execute("""SELECT * FROM Rating WHERE gID = ?""", (idv,))
                    row = self.cursor.fetchone()
                    rating = dict(metascore=row[1], user_rating=row[2],
                                   difficulty=row[3], length=row[4]) 
                    gc.set_data(rating)
                if "cheats" in info:
                    self.cursor.execute("""SELECT * FROM Codes WHERE gID = ?""", (idv,))
                    cheat = {}
                    codes = []
                    while True:
                        row = self.cursor.fetchone()
                        if row == None:
                            break
                        codes.append(cheats.Code(row[1], row[2]))
                    cheat["codes"] = codes
                    self.cursor.execute("""SELECT * FROM Unlockables WHERE gID = ?""", (idv,))
                    unlockables = []
                    while True:
                        row = self.cursor.fetchone()
                        if row == None:
                            break
                        unlockables.append(cheats.Unlockable(row[1], row[2]))
                    cheat["unlockables"] = unlockables
                    gc.set_data(cheat)
            elif isinstance(gc, company.Company):
                if "general" in info:
                    self.cursor.execute("""SELECT gID, title, platform, Info.url 
                                        FROM Company, Info WHERE cID = ? and gID 
                                        in (SELECT gID FROM Link WHERE cID = ?)""", 
                                        (idv, idv))
                    general = {}
                    games = []
                    while True:
                        row = self.cursor.fetchone()
                        if row == None:
                            break
                        games.append(game.Game(row[3], dict(title=row[1], platform=row[2]),
                                                   objID=row[0]))
                    general["games"] = games
                    gc.set_data(general)
    
        else:
             # then the game was obtained from web server        
            super(GameFaqsDB, self).update(gc, info) 
                   
    def disconnect(self):
        """Close cursor object and database connection."""
        self.cursor.close()
        self.db.close()

    
    
    
        
    