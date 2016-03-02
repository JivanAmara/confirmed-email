======================
Confirmed Email Sender
======================

This package provides a class "ConfirmedEmailMessage" derived from
the django standard class "EmailMultiAlternatives".

This class sends email only to confirmed addresses and automatically sends confirmation
messages to unconfirmed addresses.  It handles the confirmation process via a url in the
message.

Messages for unconfirmed addresses will be queued until the address is confirmed
or a timeout period defaulting to 3 days elapses.

This app is configured with the same settings as EmailMultiAlternatives plus
EMAIL_CONFIRMATION_WAIT which is an integer specifying the number of days to keep
queued messages for an unconfirmed address before deleting them.  This setting
defaults to 3.

For developers, ConfirmedEmailMessage differs from EmailMultiAlternatives with
the return value of ConfirmedEmailMessage.send().  Instead of EmailMultiAlternatives.send()
return value of 0/1 to indicate failure/success there can be a different status for each
destination address.   ConfirmedEmailMessage.send() returns, instead, a dictionary with
each destination address as a key and a state represented a string; see the documentation
for sender.ConfirmedEmailMessage'sent' for details.  This allows developers to
display a message asking a user to confirm their email address if appropriate.

settings variables:

EMAIL_CONFIRMATION_WAIT: Number of days to wait between sending confirmation emails.
    Defaults to 3 days.

EMAIL_CONFIRMATION_TEMPLATE: Template to use as the body of confirmation emails.
    It's important for this template to contain a link for the user to click on
    passed to the template via variable {{confirmation_link}}.  See default template
    'confirmed_email/confirmation_email.txt' for an example.
