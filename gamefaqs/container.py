"""
Container object for Game and Company classes.

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


class _Container(object):
    """Base class for Game and Company classes."""
    
    # default information sets retrieved
    default_info = ("main")
    
    # all information sets available
    all_info = ()
    
    # all available keys
    all_keys = ()
    
    # all mappings of infoset -> keys
    mappings = dict()
    
    def __init__(self, url, data, objID=None):
        self.url = url
        self.set_data(data, override=True)
        self.current_info = ["main"]
        self._objID = objID
    
    def set_data(self, data, override=False):
        """Set the game data to the given dictionary. If override is
        set, the previous data is removed, otherwise the two dictionary
        are merged.
        """
        if not override:
            self.data.update(data)
        else:
            self.data = data
    
    def __getitem__(self, key):
        """Return the value for a given key. A KeyError exception is raised 
        if the key is not found.
        """
        return self.data[key]
            
    def __setitem__(self, key, item):
        """Directly store the item with the given key."""
        self.data[key] = item
    
    def __delitem__(self, key):
        """Remove the given key.  A KeyError exception is raised 
        if the key is not found.
        """
        del self.data[key]
        
    def __len__(self):
        """Number of items in the data dictionary."""
        return len(self.data)
        
    def __eq__(self, other):
        """Return whether two objects are equivalent.  The criteria for 
        equivalence is webpage url.
        """
        if self.url == other.url:
            return True
        else:
            return False
    
    def get_id(self):
        """Return object id."""
        return self._objID
        
    def set_id(self, Id):
        """Set object id."""
        self._objID = Id
        
    def get_class_name(self):
        """Return the class name."""
        return self.__class__.__name__
        
    def get_keys(self):
        """Return the list of current keys."""
        return self.data.keys()
    
    def has_key(self, key):
        """Return True if the given key is defined."""
        try:
            self.__getitem__(key)
        except KeyError:
            return False
        return True
    
    def get_current_info(self):
        """Return the current set of information retrieved."""
        return self.current_info
    
    def has_current_info(self, item):
        """Return true if the given information set is in the list."""
        return item in self.current_info
    
    def add_to_current_info(self, val):
        """Add the information set to the current list."""
        if val not in self.current_info:
            self.current_info.append(val)    
    
    def get_infoset_keys(self, name):
        """Return the keys of the infoset."""
        if self.mappings.has_key(name):
            return self.mappings[name]
        else:
            raise KeyError
    
    def summary():
        """Return a summary of the object."""
        raise NotImplementedError("Override this method")
    
    