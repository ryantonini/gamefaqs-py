#!/usr/bin/python
"""
Uploads data to game_faqs database.  For internal use only.

Created on Wed Jul 15 00:52:37 2015
@author: ryantonini
"""
import time

import parse
import info
import access


def upload(platform_id):
    """Upload games info for a particular platform to the database."""
    gl = parse.ParseGameList(platform_id)
    gl.crawl()
    fi = info.FetchInfo(gl.game_urls)
    queue = fi.fetch_parallel()
    db_access = access.GameFaqs()
    while not queue.empty():
           value = queue.get()
           db_access.insert(value)
    db_access.exit()
 
       
if __name__ == '__main__':
    
    pid = parse.ParsePlatformId()
    # get list of ids for each platform
    ids = pid.find_all()
    j = ids[0]
    start = time.time()
    upload(j)
    end = time.time()
    print "Runtime: ", end-start
