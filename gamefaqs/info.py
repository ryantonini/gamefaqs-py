"""
Fetch game/company info.

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

import company
import game
import cheats
import helper

        
class FetchInfo(object):
    """Extracts game/company info from webpage."""
    
    def __init__(self):
        self.url = None
        self.soup = None
    
    def save(self, url):
        """Save bs4 object of url webpage."""
        self.url = url
        self.soup = helper.get_bs4(url)
    
    def remove(self):
        """Remove bs4 object of url webpage."""
        self.url = None
        self.soup = None
    
    def find_game_keys(self, infosets):
        """Returns the game keys, values for the given infosets."""
        info = {}
        if "general" in infosets:
            # get game esrb rating 
            for tag in self.soup.find_all("span"):
                if tag.has_attr("class") and "esrb_logo" in tag['class']:
                    info["esrb"] = tag.get_text()[:-3] # remove whitespaces and other char            
            # get game description
            desc = self.soup.find("div", {"class": "desc"}).get_text()
            desc = " ".join(desc.split()) # remove newlines
            info["description"] = desc.replace("'", "")
            # get game platform long
            info["platform_long"] =  self.soup.find("li", {"class": "core-platform"}).get_text()
            companies = []
            for tag in self.soup.find_all("a"):
                if tag.has_attr("href"):
                    # get game release date
                    if tag["href"].endswith("/data") and tag.get_text() != "Release Data":
                        info["release_date"] = tag.get_text()[:-2] # removes whitespace and >>
                    if "/features/company/" in tag['href']:
                        company_name = tag.get_text().replace("'", "''")
                        url = helper.gamefaqsURL_base + tag["href"]
                        companies.append(company.Company(url, dict(name=company_name)))
            # get game companies
            info["companies"] = companies
        
        if "rating" in infosets:
            for tag in self.soup.find_all("a"):
                if tag.has_attr("href"):
                    # get user rating 
                    if tag["href"].endswith("rate"):
                        info["user_rating"] = tag.get_text()[:-4] # remove whitespaces and other char
                    # get game difficulty
                    if tag["href"].endswith("diff"):
                        info["difficulty"] = tag.get_text()
                    # get game length (hrs)
                    if tag["href"].endswith("time"):
                        info["length"] = tag.get_text()[:-6] # remove whitespace and 'hours'             
            # get game metacritic score
            metascore_tag = self.soup.find_all("div", {'class':'score metacritic_mid'}) + \
                            self.soup.find_all("div", {'class':'score metacritic_high'}) + \
                            self.soup.find_all("div", {'class':'score metacritic_low'})
            if metascore_tag:
                info["metascore"] = metascore_tag[0].get_text()
        
        if "cheats" in infosets:
            codes = []
            unlockables = []
            url_full = self.url + "/cheats"
            bsoup = helper.get_bs4(url_full)
            table_tags = bsoup.find_all("table")
            for t in table_tags:
                if t.find_all("th", text="Code"):
                    for i in t.find_all("tr")[1:]:
                        val = i.contents
                        effect = val[0].text
                        code = val[1].text
                        codes.append(cheats.Code(effect, code))
                elif t.find_all("th", text="Unlockable"):
                    for j in t.find_all("tr")[1:]:
                        val = j.contents
                        unlockable = val[0].text
                        howto = val[1].text
                        unlockables.append(cheats.Unlockable(unlockable, howto))
            info["codes"] = codes
            info["unlockables"] = unlockables
        return info
    
    def find_company_keys(self, infosets): 
        """Return the company keys,values for the given infoset."""
        info = {}
        if "general" in infosets:
            games = []
            web_tag = self.soup.find("div", {"class": "details"})
            if web_tag and "http" in web_tag.text:
                http_index = web_tag.text.find("http")
                info["website_address"] = web_tag.text[http_index:-1]
            tables = self.soup.find_all("table")[1:]
            for t in tables:
                item = t.find("th", {"class":"genrehead"})
                if item and item.text.isdigit():
                    for gt in t.find_all("tr"):
                        if len(gt.contents) > 1:
                            children = gt.findChildren()
                            platform = children[0].text
                            title = children[1].text.replace("\n", "")
                            url = helper.gamefaqsURL_base + gt.find("a")["href"]
                            games.append(game.Game(url, dict(title=title,
                                                    platform=platform)))
                else: break
            info["games"] = games
        return info
                        
         
            
            
        
        
    