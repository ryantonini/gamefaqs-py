# -*- coding: utf-8 -*-
"""
Access to game info.

Created on Sun Aug  9 19:58:51 2015
@author: ryantonini
"""

class Game(object):
    """Provides access to the info it contains with a dictionary-like interface
    like "gameObj[key]" where key specifies the string identifier for the piece 
    of information you want to get.
    """
    
    def __init__(self, game_id, title, description, platform, release_date, esrb):
        data = {}
        data["game_id"] = game_id
        data["title"] = title
        data["description"] = description
        data["platform"] = platform
        data["release_date"] = release_date
        data["esrb"] = esrb
        self.data = data   
    
    def update(self, cursor, val=["Company", "Rating"]):
        """Updates the game information.  The default update will add company
        and rating information to the game dictionary interface.

        :param cursor Cursor for database traversal.
        :param val List containing data that we want updated.
        """
        company_list = []
        if "Company" in val:
            cursor.execute("SELECT company_name FROM Company WHERE gID = ?", (self.data["game_id"],))
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                company_list.append(row[0])
            self.data["company"] = company_list
        if "Rating" in val:
            cursor.execute("SELECT * FROM Rating WHERE gID = ?", (self.data["game_id"],))
            row = cursor.fetchone()
            self.data["metascore"] = row[1]
            self.data["user_rating"] = row[2]
            self.data["difficulty"] = row[3]
            self.data["length"] = row[4]
                
        
    def __str__(self):
        return self.data["title"] + " (" + self.data["platform"] + ")"
    
    def __repr__(self):
        return self.data["title"] + " (" + self.data["platform"] + ")"
            
                          
                     
    