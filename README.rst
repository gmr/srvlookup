srvlookup
=========
A small wrapper for dnspython to return SRV records for a given host, protocol,
and domain name as a list of namedtuples.

|Version| |Status| |Downloads|

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

Testing
-------
.. code:: bash

    python setup.py nosetests


Requirements
------------

-  `dnspython <https://pypi.python.org/pypi/dnspython>`_

.. |Version| image:: https://img.shields.io/pypi/v/srvlookup.svg?
   :target: https://pypi.python.org/pypi/srvlookup

.. |Status| image:: https://img.shields.io/travis/gmr/srvlookup.svg?
   :target: https://travis-ci.org/gmr/srvlookup

.. |Downloads| image:: https://img.shields.io/pypi/dm/srvlookup.svg?
   :target: https://pypi.python.org/pypi/srvlookup
