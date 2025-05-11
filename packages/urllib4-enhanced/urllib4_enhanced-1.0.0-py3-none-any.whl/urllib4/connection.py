"""
HTTP connection handling for urllib4.

This module provides classes for handling HTTP connections.
"""

from __future__ import annotations

import http.client
import logging
import socket
import ssl
import typing

log = logging.getLogger(__name__)


class HTTPConnection(http.client.HTTPConnection):
    """
    HTTP connection that supports additional features.
    
    This class extends the standard library's HTTPConnection with
    additional features.
    """
    
    def __init__(
        self,
        host,
        port=None,
        timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
        source_address=None,
        blocksize=8192,
    ):
        """
        Initialize a new HTTPConnection.
        
        :param host: Host to connect to
        :param port: Port to connect to
        :param timeout: Socket timeout
        :param source_address: Source address to bind to
        :param blocksize: Block size for reading
        """
        super().__init__(
            host=host,
            port=port,
            timeout=timeout,
            source_address=source_address,
            blocksize=blocksize,
        )
        
    def connect(self):
        """Connect to the host and port specified in __init__."""
        return super().connect()


class HTTPSConnection(http.client.HTTPSConnection):
    """
    HTTPS connection that supports additional features.
    
    This class extends the standard library's HTTPSConnection with
    additional features.
    """
    
    def __init__(
        self,
        host,
        port=None,
        key_file=None,
        cert_file=None,
        timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
        source_address=None,
        context=None,
        blocksize=8192,
    ):
        """
        Initialize a new HTTPSConnection.
        
        :param host: Host to connect to
        :param port: Port to connect to
        :param key_file: Path to the key file
        :param cert_file: Path to the certificate file
        :param timeout: Socket timeout
        :param source_address: Source address to bind to
        :param context: SSL context
        :param blocksize: Block size for reading
        """
        super().__init__(
            host=host,
            port=port,
            key_file=key_file,
            cert_file=cert_file,
            timeout=timeout,
            source_address=source_address,
            context=context,
            blocksize=blocksize,
        )
        
    def connect(self):
        """Connect to the host and port specified in __init__."""
        return super().connect()


class DummyConnection:
    """
    Dummy connection that does nothing.
    
    This class is used as a placeholder for connections that don't
    need to do anything.
    """
    
    def __init__(self):
        """Initialize a new DummyConnection."""
        pass
        
    def close(self):
        """Close the connection."""
        pass


# Exceptions for backwards compatibility
class HTTPException(Exception):
    """Base exception for HTTP errors."""
    pass
