import mock
import unittest

from dns import message, name, resolver

import srvlookup


class WhenRaisingException(unittest.TestCase):
    def test_should_output_exception_string(self):
        msg = 'NXDOMAIN'
        x = srvlookup.SRVQueryFailure(msg)
        self.assertEqual(str(x)[-len(msg):], msg)


class WhenLookingUpRecords(unittest.TestCase):
    def get_message(self, additional_answers=None):
        message_body = [
            'id 1234',
            'opcode QUERY',
            'rcode NOERROR',
            'flags QR AA RD',
            ';QUESTION',
            'foo.bar.baz. IN SRV',
            ';ANSWER',
            'foo.bar.baz. 0 IN SRV 2 0 11211 foo1.bar.baz.',
            'foo.bar.baz. 0 IN SRV 1 0 11212 foo2.bar.baz.',
        ]
        message_body.extend(additional_answers or [])
        message_body.extend([
            ';ADDITIONAL',
            'foo1.bar.baz.  5 IN A 1.2.3.4',
            'foo2.bar.baz.  5 IN A 1.2.3.5',
        ])
        return message.from_text('\n'.join(message_body))

    def test_should_return_a_list_of_records(self):
        with mock.patch('dns.resolver.query') as query:
            query_name = name.from_text('foo.bar.baz.')
            msg = self.get_message()
            answer = resolver.Answer(query_name, 33, 1, msg, msg.answer[0])
            query.return_value = answer
            self.assertEqual(
                srvlookup.lookup('foo', 'bar', 'baz'), [
                    srvlookup.SRV('1.2.3.5', 11212, 1, 0, 'foo2.bar.baz'),
                    srvlookup.SRV('1.2.3.4', 11211, 2, 0, 'foo1.bar.baz')
                ])

    def test_should_include_local_domain_when_omitted(self):

        with mock.patch('dns.resolver.query') as query:
            with mock.patch('socket.getfqdn') as getfqdn:
                getfqdn.return_value = 'baz'
                query_name = name.from_text('foo.bar.baz.')
                msg = self.get_message()
                answer = resolver.Answer(query_name, 33, 1, msg, msg.answer[0])
                query.return_value = answer
                self.assertEqual(
                    srvlookup.lookup('foo', 'bar'), [
                        srvlookup.SRV('1.2.3.5', 11212, 1, 0, 'foo2.bar.baz'),
                        srvlookup.SRV('1.2.3.4', 11211, 2, 0, 'foo1.bar.baz')
                    ])

    def test_should_sort_records_by_priority_weight_and_host(self):

        with mock.patch('dns.resolver.query') as query:
            query_name = name.from_text('foo.bar.baz.')
            msg = self.get_message(additional_answers=[
                'foo.bar.baz. 0 IN SRV 0 0 11213 foo3.bar.baz.'
            ])
            answer = resolver.Answer(query_name, 33, 1, msg, msg.answer[0])
            query.return_value = answer
            self.assertEqual(
                srvlookup.lookup('foo', 'bar'), [
                    srvlookup.SRV('foo3.bar.baz', 11213, 0, 0, 'foo3.bar.baz'),
                    srvlookup.SRV('1.2.3.5', 11212, 1, 0, 'foo2.bar.baz'),
                    srvlookup.SRV('1.2.3.4', 11211, 2, 0, 'foo1.bar.baz')
                ])

    def test_should_return_name_when_addt_record_is_missing(self):
        with mock.patch('dns.resolver.query') as query:
            query_name = name.from_text('foo.bar.baz.')
            msg = self.get_message(additional_answers=[
                'foo.bar.baz. 0 IN SRV 3 0 11213 foo3.bar.baz.'
            ])
            answer = resolver.Answer(query_name, 33, 1, msg, msg.answer[0])
            query.return_value = answer
            self.assertEqual(
                srvlookup.lookup('foo', 'bar', 'baz'), [
                    srvlookup.SRV('1.2.3.5', 11212, 1, 0, 'foo2.bar.baz'),
                    srvlookup.SRV('1.2.3.4', 11211, 2, 0, 'foo1.bar.baz'),
                    srvlookup.SRV('foo3.bar.baz', 11213, 3, 0, 'foo3.bar.baz')
                ])


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
                              srvlookup._query_srv_records, 'foo.bar.baz')

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
            self.assertEqual(
                srvlookup._query_srv_records('foo.bar.baz'), answer)
