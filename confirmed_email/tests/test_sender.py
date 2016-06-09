'''
Created on Feb 25, 2016

@author: jivan
'''
from datetime import datetime, timedelta

from django.core.mail.message import EmailMultiAlternatives, EmailMessage
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
        mock_send_unconfirmed.assert_called_once_with()
        expected_results = {recipient_address: 'queued'}
        self.assertEqual(send_results, expected_results)

    @mock.patch.object(ConfirmedEmailMessage, '_send_unconfirmed')
    @mock.patch.object(EmailMultiAlternatives, 'send')
    def test_send_known(self, mock_django_send, mock_send_unconfirmed):
        ''' | *brief*: Check that a message sent to a known address returns {<address>: 'sent'}
            | *author*: Jivan
            | *created*: 2016-02-25
        '''
        recipient_address = 'noone@nowhere.com'
        sender_address = 'sender@nowhere.com'
        message_subject = 'Greeting'
        message_content = 'Hi there'

        AddressConfirmation.objects.create(
            address=recipient_address, confirmation_timestamp=datetime.now()
        )
        cem = ConfirmedEmailMessage(
            subject=message_subject, body=message_content, from_email=sender_address,
            to=[recipient_address]
        )

        send_results = cem.send()
        expected_results = {recipient_address: 'sent'}
        self.assertEqual(send_results, expected_results)
        mock_send_unconfirmed.assert_not_called()


    @mock.patch.object(EmailMessage, 'send')
    def test_send_combination(self, mock_em_send):
        ''' | *brief*: Check that a message sent to a combination of known & unknown addresses
            |    returns a dictionary with appropriate statuses for each address.
        '''
        mock_em_send.return_value = 1
        known_addresses = [
            'k1@nowhere.com',  # Not yet confirmed
            'k2@nowhere.com',  # Confirmed
        ]
        # Make records to indicate the known addresses are known.
        yesterday = datetime.today() - timedelta(days=1)
        AddressConfirmation.objects.create(address=known_addresses[0], last_request_date=yesterday)
        AddressConfirmation.objects.create(address=known_addresses[1], confirmation_timestamp=yesterday)

        unknown_addresses = [
            'u1@nowhere.com',  # Address currently unknown
            'u2@nowhere.com',  # Address currently unknown
        ]
        sender_address = 'from@nowhere.com'

        recipient_addresses = known_addresses + unknown_addresses
        cem = ConfirmedEmailMessage(
            subject='Subject', body='message_body', from_email=sender_address,
            to=recipient_addresses
        )
        send_results = cem.send()

        # One call for each of the confirmation emails sent for unkown_addresses
        #    plus one call for the email sent to the confirmed address.
        self.assertEqual(mock_em_send.call_count, 3)
        self.assertEqual(set(send_results.keys()), set(known_addresses + unknown_addresses))
        expected_results = {
                'k1@nowhere.com': 'queued',
                'k2@nowhere.com': 'sent',
                'u1@nowhere.com': 'queued',
                'u2@nowhere.com': 'queued',
        }
        self.assertEqual(send_results, expected_results)
