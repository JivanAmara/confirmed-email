'''
Created on Feb 25, 2016

@author: jivan
'''
from django.test import TestCase
import mock

from confirmed_email.models import AddressConfirmation
from confirmed_email.sender import ConfirmedEmailMessage


class ConfirmedEmailMessageTests(TestCase):

    @mock.patch.object(ConfirmedEmailMessage, '_send_unconfirmed')
    def test_send_unknown(self, mock_send_unconfirmed):  # , mock_emailmultialternatives_send):
        ''' | *brief*: Checks that a message sent to an unknown address
            |    returns {<address>: 'queued'}
            | *author*: Jivan
            | *created*: 2016-02-25
        '''
        recipient_address = 'noone@nowhere.com'
        sender_address = 'sender@nowhere.com'
        message_subject = 'Greeting'
        message_content = 'Hi there'

        cem = ConfirmedEmailMessage(
            subject=message_subject, body=message_content, from_email=sender_address,
            to=[recipient_address]
        )

        # Assume successful confirmation email sending
        mock_send_unconfirmed.return_value = 1
        send_results = cem.send()
        mock_send_unconfirmed.assert_called_once_with(cem)
        expected_results = {recipient_address: 'queued'}
        self.assertEqual(send_results, expected_results)

    @mock.patch.object('sender.AddressConfirmation', 'objects.filter')
    def test_send_known(self, mock_ac_objects_filter):
        ''' | *brief*: Check that a message sent to a known address returns {<address>: 'sent'}
            | *author*: Jivan
            | *created*: 2016-02-25
        '''
        self.fail('test implementation not completed')
        recipient_address = 'noone@nowhere.com'
        sender_address = 'sender@nowhere.com'
        message_subject = 'Greeting'
        message_content = 'Hi there'

        cem = ConfirmedEmailMessage(
            subject=message_subject, body=message_content, from_email=sender_address,
            to=[recipient_address]
        )

        # Assume the address is already confirmed
        confirmed_query_entry = object()
        confirmed_query_entry.address = sender_address
        confirmed_query_result = [confirmed_query_entry]

        mock_ac_objects_filter.return_value = confirmed_query_result
        send_results = cem.send()
        expected_results = {recipient_address: 'queued'}
        self.assertEqual(send_results, expected_results)
        self.fail('Test not implemented')

    def test_send_combination(self):
        ''' | *brief*: Check that a message sent to a combination of known & unknown addresses
            |    returns a dictionary with appropriate statuses for each address.
        '''
        self.fail('Test not implemented')

    def test_send_unconfirmed(self):
        self.fail('Test not implemented')
