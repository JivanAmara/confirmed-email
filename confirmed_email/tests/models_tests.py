'''
Created on Feb 11, 2016

@author: jivan
'''
from __future__ import unicode_literals
from django.test import TestCase
from confirmed_email.sender import ConfirmedEmailMessage
from confirmed_email.models import QueuedEmailMessage, AddressConfirmation

class TestQueuedEmailMessages(TestCase):

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
