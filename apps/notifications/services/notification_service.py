from apps.notifications.models import Notification
from integrations.sms.provider import SMSProvider

class NotificationService:
    @classmethod
    def notify_user(cls, user, message, channel='SMS'):
        notif = Notification.objects.create(
            user=user,
            channel=channel,
            body=message
        )
        if channel == 'SMS' and user.phone:
            SMSProvider.send_sms(user.phone, message)
        return notif

    @classmethod
    def get_user_notifications(cls, user):
        return Notification.objects.filter(user=user).order_by('-sent_at')
