from rest_framework import serializers
from apps.notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'channel', 'body', 'is_read', 'sent_at']
        read_only_fields = ['id', 'sent_at']
