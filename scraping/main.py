#!/usr/bin/python
"""
Uploads data to game_faqs database.  For internal use only.

Created on Wed Jul 15 00:52:37 2015
@author: ryantonini
"""
import time

import parse
import access
import database_builder as db

def upload(platform, platform_id):
    """Upload games info for a particular platform to the database."""
    gl = parse.ParseGameList(platform, platform_id)
    gl.crawl()
    builder = db.Extraction(gl.games)
    queue = builder.fetch_parallel()
    db_access = access.GameFaqsDB()
    while not queue.empty():
           value = queue.get()
           db_access._insert(value)
    db_access.disconnect()
    
       
if __name__ == '__main__':
    
    pid = parse.ParsePlatformId()
    # get list of ids for each platform
    ids = pid.find_all()
    # 0, 1, 4
    j = ids[5]
    start = time.time()
    upload("DS", j)
    end = time.time()
    print "Runtime: ", end-start
