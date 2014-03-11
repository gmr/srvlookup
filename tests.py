import mock
from dns import message, name, resolver
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import srvlookup


class WhenRaisingException(unittest.TestCase):

    def test_should_output_exception_string(self):
        msg = 'NXDOMAIN'
        x = srvlookup.SRVQueryFailure(msg)
        self.assertEqual(str(x)[-len(msg):], msg)


class WhenLookingUpRecords(unittest.TestCase):

    MESSAGE = """\
id 1234
opcode QUERY
rcode NOERROR
flags QR AA RD
;QUESTION
foo.bar.baz. IN SRV
;ANSWER
foo.bar.baz. 0    IN  SRV 2 0 11211 1.2.3.4.
foo.bar.baz. 0    IN  SRV 1 0 11211 1.2.3.5.
"""

    def test_should_return_a_list_of_records(self):
        with mock.patch('dns.resolver.query') as query:
            query_name = name.from_text('foo.bar.baz.')
            msg = message.from_text(self.MESSAGE)
            answer = resolver.Answer(query_name,
                                     33, 1, msg,
                                     msg.answer[0])
            query.return_value = answer
            self.assertEqual(srvlookup.lookup('foo', 'bar', 'baz'),
                             [srvlookup.SRV('1.2.3.5', 11211, 1, 0),
                              srvlookup.SRV('1.2.3.4', 11211, 2, 0)])

    def test_should_include_local_domain_when_omitted(self):

        with mock.patch('dns.resolver.query') as query:
            with mock.patch('socket.getfqdn') as getfqdn:
                getfqdn.return_value = 'baz'
                query_name = name.from_text('foo.bar.baz.')
                msg = message.from_text(self.MESSAGE)
                answer = resolver.Answer(query_name,
                                         33, 1, msg,
                                         msg.answer[0])
                query.return_value = answer
                self.assertEqual(srvlookup.lookup('foo', 'bar'),
                                 [srvlookup.SRV('1.2.3.5', 11211, 1, 0),
                                  srvlookup.SRV('1.2.3.4', 11211, 2, 0)])


class WhenInvokingGetDomain(unittest.TestCase):

    EXPECTATION = 'bar.baz.qux'
    VALUE = 'foo.bar.baz.qux'

    def test_should_return_domain_part_only(self):
        with mock.patch('socket.getfqdn') as getfqdn:
            getfqdn.return_value = self.VALUE
            self.assertEqual(srvlookup._get_domain(), self.EXPECTATION)


class WhenInvokingQuerySRVRecords(unittest.TestCase):

    def test_invalid_should_raise_srv_query_failure(self):
        with mock.patch('dns.resolver.query') as query:
            query.side_effect = resolver.NXDOMAIN()
            self.assertRaises(srvlookup.SRVQueryFailure,
                              srvlookup._query_srv_records,
                              'foo.bar.baz')

    def test_resolver_query_should_be_invoked_with_fqdn(self):
        with mock.patch('dns.resolver.query') as query:
            query.return_value = mock.Mock('dns.resolver.Answer')
            fqdn = 'foo.bar.baz'
            srvlookup._query_srv_records(fqdn)
            query.assert_called_once_with(fqdn, 'SRV')

    def test_should_return_resolver_answer(self):
        with mock.patch('dns.resolver.query') as query:
            answer = mock.Mock('dns.resolver.Answer')
            query.return_value = answer
            self.assertEqual(srvlookup._query_srv_records('foo.bar.baz'),
                             answer)
