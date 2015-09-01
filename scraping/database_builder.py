# -*- coding: utf-8 -*-
"""
Extract game info quickly and efficiently in large bulks.

Created on Fri Aug 28 16:23:21 2015

@author: ryantonini
"""
import threading
import Queue

import access


class Extraction(object):
    """Extracts game info from webpage(s).
    
    Uses threads to improve performance when given a large number of urls.  
    Python queue is used alongside to ensure thread-safe code.
    
    :param game_urls: Dictionary of game names matched with url to the game
                      homepage.
    """
    def __init__(self, games):
        self.games = games
    
    def partition(self, size=10):
        """Returns a list of partitions.
        
        Partitions the game objects into sub-lists with each partition 
        containing the number of games specified by size.
        
        :param size: The number of elements per partition.
        """
        partitions = [self.games[x:x+size] for x in xrange(0, len(self.games), size)]
        return partitions
    
    def read_urls(self, partition, queue):
        """Open each url, extract the game info and put it into the queue."""
        db_access = access.GameFaqs()
        for game in partition:
            db_access.update(game, info=["general", "rating", "cheats"])
            print 'Fetched from %s' % game.url # indicates successful retrievals
            queue.put(game)
    
    def fetch_parallel(self):
        """Returns a queue containing data from each game webpage.
        
        The data in the queue is fetched from multiple game webpages in 
        parallel using threads.  The join operation provides an effective 
        way to synchronize the code.
        """
        result = Queue.Queue()
        # partition the data first
        partitions = self.partition()
        threads = [threading.Thread(target=self.read_urls, args = (partition, result)) for partition in partitions]
        for t in threads:
            # starts a thread by calling read_urls method
            t.start()
        for t in threads:
            # synchronize code after
            t.join()
        return result


if __name__ == "__main__":
    pass
    