'''
Created on Feb 10, 2016

@author: jivan
'''
from datetime import datetime
import logging

from django.shortcuts import render
from django.template.context import RequestContext
from django.views.generic import TemplateView

from confirmed_email.models import AddressConfirmation, QueuedEmailMessage


logger = logging.getLogger(__name__)


class HandleConfirmationClick(TemplateView):
    template_name = 'confirmed_email/address_confirmed.html'
    def get(self, request, uuid):
        # Mark the email associated with uuid as confirmed.
        ea = AddressConfirmation.objects.get(uuid=uuid)
        ea.confirmation_timestamp = datetime.now()
        # Send any emails to this address which are waiting.
        send_queued_emails(ea)

        # Provide a page to thank the user for confirming.
        rc = RequestContext(request)
        rc.update({'email_address': ea.address})
        resp = render(self.template_name, context=rc)
        return resp


def send_queued_emails(email_address):
    if email_address.confirmation_timestamp:
        # queued emails
        qes = QueuedEmailMessage.objects.filter(email_address=email_address)
        for qe in qes:
            qe.send()
    else:
        logger.warn(
            'Attempt to send queued emails for unconfirmed address: {}'.format(email_address)
        )
