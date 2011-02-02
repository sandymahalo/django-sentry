# Email notifications backend
import datetime

from django.core.cache import cache
from django.core.email import send_mail
from django.conf import settings

from sentry.models import Message
from sentry.notifications.base import NotificationBase

class Email(NotificationBase):

    def send_notification(self):
        #check to see if a notification needs to be sent (memcached)
        if  _notify():
            _send_email()

        return

    def _notify_check(self):
        """
        Determine whether or not a notification needs to be sent,
        based on the error in question and notification thresholds
        """
        # Has a notification of this type been sent at all within
        # the amount of time specified by notification time threshold? Check cache.
        cache_key = 'sentry:notification:email:%s' % self.notification_id
        if cache.get(cache_key):
            return False

        # If this type of notification has not been sent within specified
        # time threshold, check DB to see if this current error should 
        #trigger a notification based on specified error frequency
        self.time_diff = datetime.datetime.now() - datetime.timedelta(minutes=self.notification_time_threshold)
        self.recent_errors = Message.objects.filter(
            datetime__lte=self.time_diff).count()

        # If error threshold is hit, send an email.
        if recent_errors >= self.notification_error_threshold:
            # Set in cache so this notification is not sent again prematurely
            cache.set(cache_key, 'True', self.notification_time_threshold)
            return True

    def _send_email(self):
        """
        Send email notification
        """

        subject = "SENTRY NOTIFICATION: %s errors received in %s minutes" %
            (self.recent_errors, self.time_diff)

        body = render_to_string(
                'sentry/emails/notification.txt', 
                {
                    'message': 'Just letting you know.'
                }
            )

        send_mail(
            subject,
            body,
            settings.SERVER_EMAIL,
            self.recipient,
            fail_silently=True
        )

