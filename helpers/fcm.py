import logging

from firebase_admin.messaging import Message, Notification

from fcm_django.models import FCMDevice
from django.utils.translation import gettext_lazy as _, activate, get_language

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


def broadcast_notification(node=None, data=None, event=NotificationEvent.OTHER, title=None, body=None, image=None, silent=False):
        '''
            Sends an FCM notification broadcast to all devices subscribed to topic
            If the message is silent, title and message are included in the data dictionary
        '''
        logger.info("Sending FCM broadcast...")
        try:
            data = data or {}
            data["event"] = "notification"
            data["type"] = str(event.prefix)

            # Backwards compatibility issue to send notifications to existing topic for people
            # who haven't updated the app with the multilang feature.
            topic = f"{node.shortname.lower()}_{event.prefix}"
            send_broadcast(topic, data, title(), body(), image, silent)

            current_language = get_language()
            for lang in node.enabled_langs:
                activate(lang)
                topic = f"{node.shortname.lower()}_{event.prefix}_{lang}"
                send_broadcast(topic, data, title(), body(), image, silent)

            activate(current_language)  # Activate original lang back

        except Exception as e:
            logger.error(e)


def send_broadcast(topic, data, title, body, image, silent):
    if not body and not title:
        silent = True
    if title and silent:
        data['title'] = title
    if body and silent:
        data['message'] = body

    logger.info(f"Sending message to topic: {topic}")

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

