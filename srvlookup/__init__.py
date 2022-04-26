"""
Service lookup using DNS SRV records

"""
from .main import lookup, SRV, SRVQueryFailure

__all__ = [
    'lookup', 'SRV', 'SRVQueryFailure'
]
version = __version__ = '3.0.0'
