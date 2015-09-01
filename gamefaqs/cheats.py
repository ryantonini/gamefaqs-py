"""
Unlockable and Code Items.

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


class Unlockable(object):
    """Unlockable game item"""
    
    def __init__(self, unlockable, how_to):
        self.unlockable = unlockable
        self.how_to = how_to
    
    def __repr__(self):
        return "<Unlockable: {un}>".format(un=self.unlockable)
    
    def __str__(self):
        return "Unlockable({un})".format(un=self.unlockable)
    
    def summary(self):
        print "Unlockable: {un}\nHowTo: {ht}".format(un=self.unlockable,
                                                    ht=self.how_to)
                                                    

class Code(object):
    """Cheat code item"""
    
    def __init__(self, effect, code):
        self.effect = effect
        self.code = code
        
    def __repr__(self):
        return "<Code: {ef}>".format(ef=self.effect)
    
    def __str__(self):
        return "Code({ef})".format(ef=self.effect)
    
    def summary(self):
        print "Cheat: {ef}\nCode: {cd}".format(ef=self.effect, cd=self.code)
        
        
        
        
        
        
        
        
                                                    