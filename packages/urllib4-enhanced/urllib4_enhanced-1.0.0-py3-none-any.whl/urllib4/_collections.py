"""
Collections for urllib4.

This module provides specialized container datatypes.
"""

from __future__ import annotations

import collections
import typing
from collections.abc import Mapping, MutableMapping


class HTTPHeaderDict(MutableMapping[str, str]):
    """
    A case-insensitive mapping of HTTP headers.
    
    This class allows for case-insensitive lookups of HTTP headers while
    preserving the original case of the headers.
    """
    
    def __init__(self, headers=None, **kwargs):
        """
        Initialize a new HTTPHeaderDict.
        
        :param headers: Initial headers to add
        :param kwargs: Additional headers to add
        """
        self._container = {}
        if headers is not None:
            if isinstance(headers, HTTPHeaderDict):
                self._container = headers._container.copy()
            else:
                self.extend(headers)
        if kwargs:
            self.extend(kwargs)
            
    def __getitem__(self, key):
        return self._container[key.lower()][1]
        
    def __setitem__(self, key, value):
        self._container[key.lower()] = (key, value)
        
    def __delitem__(self, key):
        del self._container[key.lower()]
        
    def __iter__(self):
        return (key for key, value in self._container.values())
        
    def __len__(self):
        return len(self._container)
        
    def __eq__(self, other):
        if not isinstance(other, Mapping):
            return False
        if not isinstance(other, HTTPHeaderDict):
            other = HTTPHeaderDict(other)
        return dict(self.lower_items()) == dict(other.lower_items())
        
    def __repr__(self):
        return f"{type(self).__name__}({dict(self.items())})"
        
    def copy(self):
        """Return a copy of this HTTPHeaderDict."""
        return HTTPHeaderDict(self)
        
    def add(self, key, value):
        """
        Add a header, preserving existing headers with the same name.
        
        :param key: The header name
        :param value: The header value
        """
        key_lower = key.lower()
        if key_lower in self._container:
            old_key, old_value = self._container[key_lower]
            self._container[key_lower] = (old_key, old_value + ", " + value)
        else:
            self._container[key_lower] = (key, value)
            
    def extend(self, headers=None, **kwargs):
        """
        Add headers from another source.
        
        :param headers: Headers to add
        :param kwargs: Additional headers to add
        """
        if headers is not None:
            if isinstance(headers, HTTPHeaderDict):
                for key, value in headers.items():
                    self.add(key, value)
            elif isinstance(headers, Mapping):
                for key, value in headers.items():
                    self.add(key, value)
            else:
                for key, value in headers:
                    self.add(key, value)
        if kwargs:
            for key, value in kwargs.items():
                self.add(key, value)
                
    def getlist(self, key):
        """
        Get all values for a header as a list.
        
        :param key: The header name
        :return: List of values for the header
        """
        key_lower = key.lower()
        if key_lower not in self._container:
            return []
        return self._container[key_lower][1].split(", ")
        
    def lower_items(self):
        """Get all headers as lowercase key-value pairs."""
        return ((key.lower(), value) for key, value in self.items())
