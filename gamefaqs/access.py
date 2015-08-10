#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Database access.

Created on Thu Jul 16 12:44:44 2015
@author: ryantonini
"""
import sqlite3

import game


class GameFaqs(object):
    """Enables access to the gamefaqs database.  An instance of this class can be 
       used to search for a given title and to retrieve information about the 
       referred game."""

    def __init__(self):
        """Connect to the db"""
        self.db = sqlite3.connect("gamefaqs.db")
        self.cursor = self.db.cursor()

    def _insert(self, info):
        """Add game info to database."""
        insert_info = """INSERT INTO INFO(title, description,
                 platform, release_date, esrb)
                  VALUES ('%s', '%s', '%s', '%s', '%s')""" % \
                  (info["name"], info["description"], info["platform"],
                      info["release_date"], info["esrb"])
        insert_rating = """INSERT INTO RATING(metascore, user_rating,
                 difficulty, length)
                  VALUES ('%s', '%s', '%s', '%s')""" % \
                  (info["metascore"], info["user_rating"], info["difficulty"],
                      info["length"])
        try:
            # execute sql commands
            self.cursor.execute(insert_info)
            self.cursor.execute(insert_rating)
            game_id = self.cursor.lastrowid
            for co in info['companies']:
                insert_co = """INSERT INTO COMPANY(gID, company_name)
                    VALUES ('%s', '%s')""" % (game_id, co)
                self.cursor.execute(insert_co)
            # commit changes in the database (either commit all or none)
            self.db.commit()
        except Exception, e:
            # for debugging
            print "Database Upload Failed. Game:", info['name']
            print str(e)
            # rollback in case of an error
            self.db.rollback()


    def searchGame(self, title):
        """Searches the database for all games with the given title.

        :param title The game title.
        :returns: List of Game objects containing only basic information like
                  the game title, platform and release date.
        """
        all_games = []
        self.cursor.execute("SELECT * FROM Info WHERE title = ?", (title,))
        while True:
            row = self.cursor.fetchone()
            if row == None:
                break
            g = game.Game(row[0], row[1], row[2], row[3], row[4], row[5])
            all_games.append(g)
        return all_games
        
    def searchByCompany(self, company):
        """Searches the database for all games with the given company.

        :param company: The company name.
        :returns: List of Game objects containing only basic information like
                  the game title, platform and release date.
        """
        all_games = []
        self.cursor.execute("SELECT * FROM Info WHERE gID in (SELECT gID FROM Company WHERE company_name = ?)", (company,))
        while True:
            row = self.cursor.fetchone()
            if row == None:
                break
            g = game.Game(row[0], row[1], row[2], row[3], row[4], row[5])
            all_games.append(g)
        return all_games

    def searchByPlatform(self, platform, esrb=""):
        """Searches the database for all games in the given platform.
        An optional argument can be specified for esrb rating to filter the
        search results.

        :param platform: The platform title.
        :param esrb: Desired esrb rating (optional)
        :returns: List of Game objects containing only basic information like
                  the game title, platform and release date.
        """
        all_games = []
        if not esrb:
            self.cursor.execute("SELECT * FROM Info WHERE platform = ?", (platform,))
        else:
            self.cursor.execute("SELECT * FROM Info WHERE platform = ? and esrb = ?", (platform, esrb))
        while True:
            row = self.cursor.fetchone()
            if row == None:
                break
            g = game.Game(row[0], row[1], row[2], row[3], row[4], row[5])
            all_games.append(g)
        return all_games
        
    def disconnect(self):
        """Close cursor object and database connection."""
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    pass


