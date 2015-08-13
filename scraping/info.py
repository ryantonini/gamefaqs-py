#!/usr/bin/python
"""
Fetch game info.

Created on Sat Jul 11 19:12:58 2015
@author: ryantonini
"""
from itertools import islice
import requests
import threading
import bs4
import Queue

keys = ["name", "description", "platform", "release_date", "user_rating",
        "difficulty", "length", "esrb", "metascore", "companies"]
        
        
class FetchInfo(object):
    """Extracts game info from webpage(s).
    
    Uses threads to improve performance when given a large number of urls.  
    Python queue is used alongside to ensure thread-safe code.
    
    :param game_urls: Dictionary of game names matched with url to the game
                      homepage.
    """
    def __init__(self, game_urls):
        self.urls = game_urls
    
    def partition(self, size=15):
        """Returns a list of partitions.
        
        Partitions the urls data into sub-dictionaries with each partition 
        containing the number of items specified by size.
        
        :param size: The number of elements per partition.
        """
        partitions = []
        it = iter(self.urls)
        for i in xrange(0, len(self.urls), size):
            partitions.append({k : self.urls[k] for k in islice(it, size)})
        return partitions
    
    def get_info(self, soup, name):
        """Returns the desired info for the specified game as a dictionary.
        
        The info that gets returned includes: name, description, platform, 
        release data, companies, user rating, difficulty, length, esrb, 
        and metascore.  If a descriptor element cannot be found, its value
        will be set to 'None'.
        
        :param soup: Html source code for the game webpage
        :param name: The games' name.
        """
        info = {}
        # get game name
        info["name"] = name.replace("'", "''")
        # get game description
        desc = soup.find("div", {"class": "desc"}).get_text()
        desc = " ".join(desc.split()) # remove newlines
        info["description"] = desc.replace("'", "")
        # get game platform
        info["platform"] =  soup.find("li", {"class": "core-platform"}).get_text()
        companies = []
        for tag in soup.find_all("a"):
            if tag.has_attr("href"):
                # get game release date
                if tag["href"].endswith("/data") and tag.get_text() != "Release Data":
                    info["release_date"] = tag.get_text()[:-2] # removes whitespace and >>
                if "/features/company/" in tag['href']:
                    companies.append(tag.get_text().replace("'", "''"))
                # get user rating 
                if tag["href"].endswith("rate"):
                    info["user_rating"] = tag.get_text()[:-4] # remove whitespaces and other char
                # get game difficulty
                if tag["href"].endswith("diff"):
                    info["difficulty"] = tag.get_text()
                # get game length (hrs)
                if tag["href"].endswith("time"):
                    info["length"] = tag.get_text()[:-6] # remove whitespace and 'hours'
        # get game companies
        info["companies"] = companies
        # get game esrb rating 
        for tag in soup.find_all("span"):
            if tag.has_attr("class") and "esrb_logo" in tag['class']:
                info["esrb"] = tag.get_text()[:-3] # remove whitespaces and other char
        # get game metacritic score
        metascore_tag = soup.find_all("div", {'class':'score metacritic_mid'}) + \
                        soup.find_all("div", {'class':'score metacritic_high'}) + \
                        soup.find_all("div", {'class':'score metacritic_low'})
        if metascore_tag:
            info["metascore"] = metascore_tag[0].get_text()
        # if an element is not defined in info, define it as 'None'
        for e in keys:
            if not e in info.keys():
                info[e] = "None" 
        return info

    def read_urls(self, partition, queue):
        """Open each url, extract the game info and put it into the queue."""
        for name, url in partition.iteritems():
            data = requests.get(url).text
            soup = bs4.BeautifulSoup(data, 'html.parser')
            info = self.get_info(soup, name)
            print 'Fetched from %s' % url # indicates successful retrievals
            queue.put(info)
    
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
    
         
            
            
        
        
    