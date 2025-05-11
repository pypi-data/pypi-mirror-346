"""
Timeout handling for urllib4.

This module provides classes for handling timeouts.
"""

from __future__ import annotations

import time
import typing


class _TYPE_DEFAULT:
    """Sentinel object for default timeout values."""
    
    @property
    def connect_timeout(self):
        """Get the connect timeout."""
        return None
        
    @property
    def read_timeout(self):
        """Get the read timeout."""
        return None


class Timeout:
    """
    Timeout configuration.
    
    This class represents timeout configuration for HTTP requests.
    """
    
    # Default timeout for socket operations
    DEFAULT_TIMEOUT = _TYPE_DEFAULT()
    
    def __init__(
        self,
        total=None,
        connect=None,
        read=None,
    ):
        """
        Initialize a new Timeout.
        
        :param total: Total timeout for the request
        :param connect: Timeout for the connection
        :param read: Timeout for reading
        """
        self._connect = connect
        self._read = read
        self._total = total
        
    @classmethod
    def from_float(cls, timeout):
        """
        Create a Timeout from a float.
        
        :param timeout: Timeout value
        :return: Timeout instance
        """
        if timeout is None:
            return cls.DEFAULT_TIMEOUT
        if isinstance(timeout, Timeout):
            return timeout
        return Timeout(connect=timeout, read=timeout)
        
    @property
    def connect_timeout(self):
        """Get the connect timeout."""
        if self._connect is None:
            return self.total
        return self._connect
        
    @property
    def read_timeout(self):
        """Get the read timeout."""
        if self._read is None:
            return self.total
        return self._read
        
    @property
    def total(self):
        """Get the total timeout."""
        return self._total
