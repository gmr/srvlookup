"""
Service Lookup
==============

Use DNS SRV records to discover services by name and protocol.

"""
import collections
import logging
import socket
import typing

from dns import rdatatype, resolver

LOGGER = logging.getLogger(__name__)

SRV = collections.namedtuple(
    'SRV', ['host', 'port', 'priority', 'weight', 'hostname'])


class SRVQueryFailure(Exception):
    """Exception that is raised when the DNS query has failed."""

    def __str__(self) -> str:
        return 'SRV query failure: %s' % self.args[0]


def lookup(name: str, protocol: str = 'TCP',
           domain: typing.Optional[str] = None,
           tcp_resolver: bool = False) -> typing.List[SRV]:
    """Return a list of service records and associated data for the given
    service name, protocol and optional domain. If protocol is not specified,
    TCP will be used. If domain is not specified, the domain name returned by
    the operating system will be used.

    Service records will be returned as a named tuple with host, port, priority
    and weight attributes:

        >>> import srvlookup
        >>> srvlookup.lookup('api', 'memcached')
        [SRV(host='192.169.1.100', port=11211, priority=1, weight=0,
             hostname='host1.example.com'),
         SRV(host='192.168.1.102', port=11211, priority=1, weight=0,
             hostname='host2.example.com'),
         SRV(host='192.168.1.120', port=11211, priority=1, weight=0,
             hostname='host3.example.com'),
         SRV(host='192.168.1.126', port=11211, priority=1, weight=0,
             hostname='host4.example.com')]
        >>>

    :param name: The service name
    :param protocol: The protocol name, defaults to TCP
    :param domain: The domain name to use, defaults to local domain name

    """
    answer = _query_srv_records(
        f'_{name}._{protocol}.{domain or _get_domain()}', tcp_resolver)
    results = _build_result_set(answer)
    return sorted(results, key=lambda r: (r.priority, -r.weight, r.host))


def _get_domain() -> str:
    """Return the domain name for the local host."""
    return '.'.join(socket.getfqdn().split('.')[1:])


def _query_srv_records(fqdn: str, tcp_resolver: bool) -> resolver.Answer:
    """Query DNS for the SRV records of the fully-qualified domain name
    specified.

    :param fqdn: The fully-qualified domain name to query
    :raises: SRVQueryFailure

    """
    try:
        return resolver.resolve(fqdn, 'SRV', tcp=tcp_resolver)
    except (resolver.NoAnswer,
            resolver.NoNameservers,
            resolver.NotAbsolute,
            resolver.NoRootSOA,
            resolver.NXDOMAIN) as error:
        LOGGER.error('Error querying SRV for %s: %r', fqdn, error)
        raise SRVQueryFailure(error.__class__.__name__)


def _build_resource_to_address_map(answer: resolver.Answer) -> dict:
    """Return a dictionary that maps resource name to address.

    The response from any DNS query is a list of answer records and
    a list of additional records that may be useful.  In the case of
    SRV queries, the answer section contains SRV records which contain
    the service weighting information and a DNS resource name which
    requires further resolution.  The additional records segment may
    contain A records for the resources.  This function collects them
    into a dictionary that maps resource name to an array of addresses.

    """
    mapping = collections.defaultdict(list)
    for resource in answer.response.additional:
        target = resource.name.to_text()
        mapping[target].extend(record.address for record in resource.items
                               if record.rdtype == rdatatype.A)
    return mapping


def _build_result_set(answer: resolver.Answer) -> typing.List[SRV]:
    """Return a list of SRV instances for a DNS answer"""
    resource_map = _build_resource_to_address_map(answer)
    result_set = []
    for resource in answer:
        target = resource.target.to_text()
        if target in resource_map:
            result_set.extend(
                SRV(address, resource.port, resource.priority, resource.weight,
                    target.strip('.')) for address in resource_map[target])
        else:
            result_set.append(
                SRV(target.rstrip('.'), resource.port, resource.priority,
                    resource.weight, target.strip('.')))
    return result_set
