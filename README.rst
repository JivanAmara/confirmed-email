======================
Confirmed Email Sender
======================

This package provides a class "ConfirmedEmailMessage" derived from
the django standard class EmailMultiAlternatives.

This class sends email only to confirmed addresses and automatically sends confirmation
messages to unconfirmed addresses.  It handles the confirmation process via a url in the
message.

Messages for unconfirmed addresses will be queued until the address is confirmed
or a timeout period defaulting to 3 days elapses.

This app is configured with the same settings as EmailMultiAlternatives plus
EMAIL_CONFIRMATION_WAIT which is an integer specifying the number of days to keep
queued messages for an unconfirmed address before deleting them.  This setting
defaults to 3.
