'''
Created on Feb 10, 2016

@author: jivan
'''
import copy
from django.core.mail.message import EmailMultiAlternatives
from confirmed_email.models import AddressConfirmation, QueuedEmailMessage
import logging
logger = logging.getLogger(__name__)

class ConfirmedEmailMessage(EmailMultiAlternatives):
    def send(self, *args, **kwargs):
        destination_count = len(self.recipients())
        confirmed = AddressConfirmation.objects.filter(
                        address__in=self.recipients(),
                        confirmation_timestamp__isnull=False)
        confirmed_addresses = [ c.address for c in confirmed ]
        confirmed_count = len(confirmed_addresses)

        # If all the destination addresses are confirmed, send as-is.
        if destination_count == confirmed_count:
            ret = self.send()
        else:
            # If any of the destination addresses are unconfirmed, send to
            #    each individually.
            for recipient in self.recipients():
                cem = copy.deepcopy(self)
                if recipient in confirmed_count:
                    ret = cem.send()
                else:
                    cem.to = [recipient]
                    cem.cc = []
                    cem.bcc = []
                    ret = cem.send_unconfirmed()

        return ret

    def send_unconfirmed(self):
        if len(self.recipients()) > 1:
            msg = 'send_unconfirmed() should not be used directly.  Use send().'
            logger.error(msg)
        address = self.recipients()[0]

        # Add address to EmailAddresses
        ea = AddressConfirmation.objects.get_or_create(address=address)
        # Queue message
        qem = QueuedEmailMessage.objects.create(email_address=ea, email_contents=self)
        if not qem:
            logger.error('Unable to create QueuedEmailMessage to {}'.format(address))
        # Send confirmation email
        ea.send_confirmation_request(from_address=self.from_email)

    def __eq__(self, other):
        ret = self.__dict__ == other.__dict__
        return ret

    def __unicode__(self):
        u = u''
        for key, val in self.__dict__.items():
            u += '{}: {}\n'.format(key, val)
        return u
