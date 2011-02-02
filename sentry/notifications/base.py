# Sentry notifications base class

import hashlib

import sentry.conf as conf

class NotificationBase(object):
    """
    Base class to handle Sentry notifications
    """

    def __init__(self, notification):
        """
        Get settings from notification
        """
        self.notification_id = hashlib.sha1(repr(notification)).hexdigest()
        self.recipient = notification['options']['to']
        self.conditions = notification['conditions']
        self.notification_frequency = notification['conditions'].get('error_frequency', conf.NOTIFICATION_FREQUENCY)
        self.notification_time_threshold = notification['conditions'].get('time_threshold', conf.NOTIFICATION_TIME_THRESHOLD)
        self.notification_error_threshold = notification['conditions'].get('error_threshold', conf.NOTIFICATION_ERROR_THRESHOLD)

    def send_notification(self):
        """
        This function is implemented in the child class.
        """
        raise NotImplementedError

