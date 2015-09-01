"""
Base Parser Class.

Created on Fri Jul 10 22:01:22 2015
@author: ryantonini
"""
import bs4
import game

from selenium import webdriver

URL = "http://www.gamefaqs.com"

class Parser(object):
    """The Base Parser"""
    
    def __init__(self, url):
        self.soup = self.open_url(url)
    
    def open_url(self, url):
        """Return the html contents of a dynamic (or static) webpage given by
        url as as a beautiful soup object.
        
        :param url: The url to connect to.
        """
        driver = webdriver.Chrome()      
        driver.get(url)  
        html_source = driver.page_source  
        driver.quit()
        return bs4.BeautifulSoup(html_source,'html.parser') 
        
        
class ParsePlatformId(Parser):
    """Parse webpage for single (or multiple) platform ids.
    
    The platforms used are specified in the platforms.txt file.  This file
    should not be changed, unless specifications change.
    
    :param url: Default url value should not be changed, unless website
                content updates.
    """
    
    def __init__(self, url="http://www.gamefaqs.com/features/rankings"):
        super(ParsePlatformId, self).__init__(url)
        self.platforms = open('data/platforms.txt', 'r').read().split('\n')
    
    def find(self, platform):
        """Return platform id."""
        tag = self.soup.find("option", {"label": platform})
        return tag.attrs['value']
    
    def find_all(self):
        """Return all platform ids."""
        ids = []
        for platform in self.platforms:
            tag_id = self.find(platform)
            ids.append(tag_id)
        return ids
            
    
class ParseGameList(Parser):
    """Parse webpage(s) for game objects corresponding to the platform id specified.
    
    Provides a general way of obtaining the url to each games homepage for
    later processing and extraction of information. 
    
    :param platform_id: Specifies the platform to obtain game urls from.
    :param url_first: Default url value should not be changed.
    :param url_second: Default url value should not be changed.
    """
    
    def __init__(self, platform, platform_id, 
                 url_first="http://www.gamefaqs.com/features/rankings?platform=",
                 url_second="&genre=0&list_type=rate&view_type=0&dlc=0&min_votes=0"):
        url = url_first + str(platform_id) + url_second
        super(ParseGameList, self).__init__(url)
        self.platform = platform
        self.games = []
    
    def get_games(self):
        """Get all the game objects on the current webpage."""
        tags = self.soup.find_all("td", {'class': "rmain"})
        for tag in tags:
            if tag.findChildren("a"):
                atag = tag.findChildren("a")[0]
                if atag.has_attr("href") and atag.contents:
                    game_url = URL + atag['href']
                    self.games.append(game.Game(game_url, dict(title=atag.contents[0],
                                                               platform=self.platform)))
    
    def get_next_link(self):
        """Return the link to the next webpage.
        
        If the last page has been reached, return None.
        """
        tags = self.soup.find_all("li", {"class": None})
        for tag in tags:
            if tag.findChildren("a"):
                atag = tag.findChildren("a")[0]
                if atag.has_attr("href") and atag.contents:
                     # check if 'Next' is present in atag
                    if "Next" in atag.contents[0]:
                        return atag['href']
                    # if not 'Next', check for 'Last'
                    elif "Last" in atag.contents[0]:
                        return atag['href']
         
    def crawl(self, check_first=True):
        """Crawl through each webpage extracting game urls.
        
        :param check_first: Whether to extract game urls from starting webpage.
        """
        # get all games on first webpage
        if check_first:
            self.get_games()
        # get url to next webpage
        link = self.get_next_link()  
        # check if there is a next webpage
        if link:
            new_url = URL + link
            # open single url provided 
            self.soup = self.open_url(new_url) 
            self.get_games()
            # crawl through the next webpage if it exists
            self.crawl(check_first=False)


if __name__ == "__main__":
    pass

