'''
Created on Feb 11, 2016

@author: jivan
'''
from __future__ import unicode_literals

from datetime import date, timedelta
import os

from django.contrib.sites.models import Site
from django.core.mail.message import EmailMessage
from django.test import TestCase
import mock

from confirmed_email.models import QueuedEmailMessage, AddressConfirmation, EMAIL_CONFIRMATION_WAIT
from confirmed_email.sender import ConfirmedEmailMessage


class QueuedEmailMessageTests(TestCase):

    def test_message_serialization(self):
        to_address = 'nobody@nowhere.com'
        ac = AddressConfirmation.objects.create(address=to_address)

        cem_before = ConfirmedEmailMessage(
            to=[to_address], from_email='noone@nowhere.com', subject='Test Email',
            body='This is the message body.'
        )
        qem = QueuedEmailMessage.objects.create(address_confirmation=ac)
        qem.email_contents = cem_before
        qem.save()
        cem_after = QueuedEmailMessage.objects.get(address_confirmation=ac).email_contents
        msg = 'before:\n{}\n'.format(cem_before)
        msg += '---\n'
        msg += 'after:\n{}'.format(cem_after)
        self.assertEqual(cem_after, cem_before, msg)

    def test_attachment_serialization(self):
        to_address = 'nobody@nowhere.com'
        ac = AddressConfirmation.objects.create(address=to_address)

        binary_dirpath = os.path.normpath(os.path.join(os.path.abspath(__file__), os.path.pardir))
        binary_filepath = os.path.join(binary_dirpath, 'binary_testing_file')
        with open(binary_filepath, 'rb') as bf:
            attachment_data = bf.read()
        cem_before = ConfirmedEmailMessage(
            to=[to_address], from_email='noone@nowhere.com', subject='Test Email',
            body='This is the message body.'
        )
        cem_before.attach('attachment_file', attachment_data)
        qem = QueuedEmailMessage.objects.create(address_confirmation=ac)
        qem.email_contents = cem_before
        qem.save()

        cem_after = QueuedEmailMessage.objects.get(address_confirmation=ac).email_contents
        msg = 'before:\n{}\n'.format(cem_before)
        msg += '---\n'
        msg += 'after:\n{}'.format(cem_after)
        self.assertEqual(cem_after, cem_before, msg)


class AddressConfirmationTests(TestCase):
    @mock.patch.object(EmailMessage, 'send')
    def test_send_first_confirmation_request(self, emailmessage_send):
        emailmessage_send.return_value = 1
        # Send to unknown address.  Should send successfully.
        to_address = 'nobody@nowhere.com'
        from_address = 'from@nowhere.com'
        cem = AddressConfirmation.objects.create(address=to_address)
        result = cem.send_confirmation_request(from_address)
        self.assertEqual(result, 1)
        self.assertEqual(emailmessage_send.call_count, 1)

    @mock.patch.object(EmailMessage, 'send')
    def test_send_2nd_confirmation_request(self, emailmessage_send):
        emailmessage_send.return_value = 1
        # Send confirmation to address which had a confirmation sent yesterday.
        #    Should skip sending but return as successfully sent.
        to_address = 'nobody@nowhere.com'
        from_address = 'from@nowhere.com'
        cem = AddressConfirmation.objects.create(
                  address=to_address, last_request_date=date.today() - timedelta(days=1))
        result = cem.send_confirmation_request(from_address)
        self.assertEqual(result, 1)
        self.assertEqual(emailmessage_send.call_count, 0)

    @mock.patch.object(EmailMessage, 'send')
    def test_send_3rd_confirmation_request(self, emailmessage_send):
        print(Site.objects.count())
        emailmessage_send.return_value = 1
        # Send confirmation to address which had a confirmation sent more than
        #    EMAIL_CONFIRMATION_WAIT days ago.
        # Should send successfully.
        to_address = 'nobody@nowhere.com'
        from_address = 'from@nowhere.com'
        # EMAIL_CONFIRMATION_WAIT plus 1
        ecwp1 = EMAIL_CONFIRMATION_WAIT + 1
        cem = AddressConfirmation.objects.create(
                  address=to_address, last_request_date=date.today() - timedelta(days=ecwp1))
        result = cem.send_confirmation_request(from_address)
        self.assertEqual(result, 1)
        self.assertEqual(emailmessage_send.call_count, 1)
