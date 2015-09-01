"""
This module provides the Game class, used to store information about
a given Game.

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

from container import _Container

class Game(_Container):
    """A game.
    
    Every piece of information about a game can be accessed as:
        gameObject["info"]
    
    To view the different keys that can stored in a Game object use the 
    all_keys static variable.  To view the different information sets available 
    use the all_info class variable.  To view the keys that belong to each 
    information set use the get_infoset_keys(infoset) method or the mappings
    static variable.
     
    Information Sets:
       
          name     | keys
         ---------------------------------------------------------------------
          main     | title, platform
          general  | companies, esrb, release_date, platform_long, description
          rating   | metascore, user_rating, length, difficulty
          cheats   | codes, unlockables 
          
    """ 
    # all the sets of information available
    all_info = ("main", "general", "rating", "cheats")
    
    # all the keys available 
    all_keys = ("title", "platform", "companies", "esrb", "release_date", 
                "platform_long", "description", "metascore", "user_rating", 
                "length", "difficulty", "codes", "unlockables")   
                
    # all mappings of infoset -> keys
    mappings = dict(main=["title", "platform"], general=["companies", "esrb", 
                    "release_date", "platform_long", "description"],
                    rating=["metascore", "user_rating", "length", "difficulty"],
                    cheats=["codes", "unlockables"])
                    
    def summary(self):
        "Print a detailed view of the Game object"
        print self.__str__()
        if self.has_current_info("general"):    
           length = len(self.data["companies"])
           company_str = ""
           for i in range(length):
               if i == (length - 1):
                   company_str += self.data["companies"][i]["name"]
               else:
                   company_str += self.data["companies"][i]["name"] + ", "        
           print "\n{co}\n{rd}\n{eb}\nMetaScore: {ms}\n{d}".format(co=company_str,
                                                   rd=self.data["release_date"],
                                                   eb=self.data["esrb"],
                                                   ms=self.data["metascore"],
                                                   d=self.data["description"])
        
    def __str__(self):
        """Simply print the title with platform."""
        return self.data["title"] + " (" + self.data["platform"] + ")"
    
    def __repr__(self):
        """String representation of a Game object."""
        return "<Game0bj: {t} ({p})>".format(t=self.data["title"], 
                                            p=self.data["platform"])
    
    def view_codes(self):
        """Display each cheat code."""
        if self.has_key("codes"):
            for code in self.data["codes"]:
                print code.effect + ": " + code.code
        
    def view_unlockables(self):
        """Display each unlockable item."""
        if self.has_key("unlockables"):
            for unlockable in self.data["unlockables"]:
                print unlockable.unlockable + ": " + unlockable.how_to

    
   
    
                     
    