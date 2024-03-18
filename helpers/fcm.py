import logging

from django.conf import settings
from firebase_admin.messaging import Message, Notification

from fcm_django.models import FCMDevice
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class NotificationEvent:
    class Event:
        def __init__(self, title, prefix):
            self.title = title
            self.prefix = prefix

    OTHER = Event(_("Otro"), "other")
    NEWS_ADDED = Event(_("Nueva noticia"), "news")
    OFFER_ADDED = Event(_("Nueva oferta"), "offers")


def notify_user(user, data, event=NotificationEvent.OTHER, title=None, body=None, image=None, silent=True):
    '''
        Sends an FCM notification to a user
        If the message is silent, title and message are included in the data dictionary
    '''
    logger.info("Sending FCM notification...")

    if not user:
        return

    data = data or {}
    data["event"] = str(event.title)

    if not body and not title:
        silent = True
    if title and silent:
        data['title'] = title
    if body and silent:
        data['message'] = body

    device = FCMDevice.objects.filter(user=user).first()
    if device is None:
        return
    if silent:
        result = device.send_message(
            Message(data=data)
        )
    else:
        result = device.send_message(
            Message(notification=Notification(title=title, body=body, image=image), data=data)
        )
    logger.info(f"FCM Notification sent: {result}")


def broadcast_notification(node_shortname=None, data=None, event=NotificationEvent.OTHER, title=None, body=None, image=None, silent=False):
        '''
            Sends an FCM notification broadcast to all devices subscribed to topic
            If the message is silent, title and message are included in the data dictionary
        '''
        if not settings.DEBUG:
            logger.info("Sending FCM broadcast...")
            try:
                data = data or {}
                data["event"] = str(event.title)

                if not body and not title:
                    silent = True
                if title and silent:
                    data['title'] = title
                if body and silent:
                    data['message'] = body

                topic = node_shortname + "_" + event.prefix

                if silent:
                    result = FCMDevice.send_topic_message(
                        Message(data=data),
                        topic
                    )
                else:
                    result = FCMDevice.send_topic_message(
                        Message(notification=Notification(title=title, body=body, image=image), data=data),
                        topic
                    )
                logger.info(f"FCM Broadcast sent: {result}")
            except Exception as e:
                logger.error(e)
        else:
            logger.info(f"Simulate sending Broadcast (DEBUG mode is enabled).")

