srvlookup
=========
A small wrapper for dnspython to return SRV records for a given host, protocol,
and domain name as a list of namedtuples.

|PyPI version| |Build Status|

Installation
------------
srvlookup is available on the `Python Package Index <https://pypi.python.org/pypi/srvlookup>`_. Simply:

.. code:: bash

    pip install srvlookup

Example
-------
.. code:: python

    >>> import srvlookup
    >>> srvlookup.lookup('api', 'memcached')
    [SRV(host='192.169.1.100', port=11211, priority=1, weight=0),
     SRV(host='192.168.1.102', port=11211, priority=1, weight=0),
     SRV(host='192.168.1.120', port=11211, priority=1, weight=0),
     SRV(host='192.168.1.126', port=11211, priority=1, weight=0)]
    >>>

Requirements
------------

-  `dnspython <https://pypi.python.org/pypi/dnspython>`_

.. |PyPI version| image:: https://badge.fury.io/py/srvlookup.png
   :target: http://badge.fury.io/py/srvlookup
.. |Build Status| image:: https://travis-ci.org/aweber/srvlookup.png?branch=master
   :target: https://travis-ci.org/aweber/srvlookup
