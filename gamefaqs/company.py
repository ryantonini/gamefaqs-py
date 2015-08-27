# -*- coding: utf-8 -*-
"""
This module provides the Company class, used to store information about
a given company.

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


class Company(_Container):
    """A Company.  
    
    Every piece of information about a company can be accessed as:
        companyObject["info"]
    
    To view the different keys that can stored in a Company object use the 
    all_keys static variable.  To view the different information sets available 
    use the all_info class variable.  To view the keys that belong to each 
    information set use the get_infoset_keys(infoset) method or the mappings
    static variable.
    
    Information Sets:
       
          name     | keys
         ----------------------------------------------------------------------
          main     | name
          general  | website_address, games         
          
    """
    # all the sets of information available
    all_info = ("main", "general")
    
    # all the keys available 
    all_keys = ("name", "website_address", "games")
    
    # all mappings of infoset -> keys
    mappings = dict(main=["name"], general=["website_address", "games"])
         
    def __str__(self):
        """Simply print the company name."""
        return self.data["name"]
    
    def __repr__(self):
        """String representation of a Company object."""
        return "<CompanyObj: {n}>".format(n=self.data["name"])
    
    def summary(self):
        """Detailed view of the Company object."""
        print self.__str__() 
        if self.has_current_info("general"):
            print self.data["website_address"] 
            games = self.get_games(limit=5)
            for g in games:
                print g
            
    def get_games(self, limit=10):
        """Return a list of games.  
        
        Limit specifies the maximun number to return.      
        """
        if self.has_key("games"):
            if len(self.data["games"]) <= limit:
                return self.data["games"]
            else:
                return self.data["games"][:limit]
        
    