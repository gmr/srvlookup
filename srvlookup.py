"""
Service Lookup
==============

Use DNS SRV records to discover services by name and protocol.

"""
from collections import namedtuple
import logging
from dns import resolver
import socket

__version__ = (0, 1, 0)
version = '%s.%s.%s' % __version__

LOGGER = logging.getLogger(__name__)

SRV = namedtuple('SRV', ['host', 'port', 'priority', 'weight'])


class SRVQueryFailure(Exception):
    """Exception that is raised when the DNS query has failed."""
    def __str__(self):
        return 'SRV query failure: %s' % self.args[0]


def lookup(name, protocol='TCP', domain=None):
    """Return a list of service records and associated data for the given
    service name, protocol and optional domain. If protocol is not specified,
    TCP will be used. If domain is not specified, the domain name returned by
    the operating system will be used.

    Service records will be returned as a named tuple with host, port, priority
    and weight attributes:

        >>> import srvlookup
        >>> srvlookup.lookup('api', 'memcached')
        [SRV(host='192.169.1.100', port=11211, priority=1, weight=0),
         SRV(host='192.168.1.102', port=11211, priority=1, weight=0),
         SRV(host='192.168.1.120', port=11211, priority=1, weight=0),
         SRV(host='192.168.1.126', port=11211, priority=1, weight=0)]
        >>>

    :param str name: The service name
    :param str protocol: The protocol name, defaults to TCP
    :param str domain: The domain name to use, defaults to local domain name
    :rtype: list of srvlookup.SRV

    """
    answer = _query_srv_records('_%s._%s.%s' % (name, protocol,
                                                domain or _get_domain()))
    return sorted([SRV(str(record.target).rstrip('.'),
                       record.port,
                       record.priority,
                       record.weight) for record in answer],
                  key=lambda r: r.priority)

def _get_domain():
    """Return the domain name for the local host.

    :rtype: str

    """
    return '.'.join(socket.getfqdn().split('.')[1:])


def _query_srv_records(fqdn):
    """Query DNS for the SRV records of the fully-qualified domain name
    specified.

    :param str fqdn: The fully-qualified domain name to query
    :rtype: dns.resolver.Answer
    :raises: SRVQueryFailure

    """
    try:
        return resolver.query(fqdn, 'SRV')
    except (resolver.NoAnswer,
            resolver.NoNameservers,
            resolver.NotAbsolute,
            resolver.NoRootSOA,
            resolver.NXDOMAIN) as error:
        LOGGER.error('Error querying SRV for %s: %r', fqdn, error)
        raise SRVQueryFailure(error.__class__.__name__)
