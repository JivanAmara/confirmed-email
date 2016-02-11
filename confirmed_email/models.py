'''
Created on Feb 10, 2016

@author: jivan
'''
import base64
import cPickle
from cStringIO import StringIO
import uuid

from django.core.mail.message import EmailMessage
from django.core.urlresolvers import reverse
from django.db import models
from django.shortcuts import render


class EmailAddresses(models.Model):
    ''' Stores addresses with their confirmation status. '''
    address = models.EmailField()
    # unique string used as part of the confirmation link.
    uuid = models.CharField(max_length=32, default=uuid.uuid1)
    # This is None for unconfirmed addresses or the timestamp when the user clicked
    #    the confirmation link.
    confirmation_timestamp = models.DateTimeField()
    last_request_date = models.DateField()
    request_count = models.IntegerField()

    def send_confirmation_request(self, from_address):
        confirmation_link = reverse('confirmation_url', {'guid': self.guid})
        message_context = {'confirmation_link': confirmation_link}
        message_body = render('confirmed_email/email.txt', message_context)
        message_body = message_body.content()

        # Confirmation Email
        ce = EmailMessage(subject='Please confirm your email address',
                          body=message_body,
                          from_email=from_address,
                          to=self.address)


class EmailMessages(models.Model):
    ''' Stores unsent email messages while waiting for confirmation.'''
    email_address = models.ForeignKey(EmailAddresses)
    # Date when the message was queued while awaiting confirmation.
    date = models.DateField(auto_now=True)
    # ConfirmedEmailMessage instance serialized with json-pickle.
    _email_contents = models.TextField(db_column='email_contents', blank=True)

    def set_email_contents(self, email_message):
        # --- Pickle & encode the message for storage in a TextField.
        # In-memory pickle output.
        po = StringIO()
        cPickle.dump(email_message, po)
        pickle_output = po.getvalue()
        po.close()

        self._email_contents = base64.encodestring(pickle_output)

    def get_email_contents(self):
        # --- Decode & unpickle the message
        pickle_input = base64.decodestring(self._email_contents)
        # In-memory pickle input
        pi = StringIO(pickle_input)
        message = cPickle.load(pi)

        return message
