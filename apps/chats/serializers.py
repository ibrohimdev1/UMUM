from rest_framework import serializers
from apps.chats.models import Chat, Message
from apps.accounts.serializers.user_serializer import UserSerializer
from apps.listings.serializers import ListingListSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'body', 'is_read', 'sent_at']

class ChatSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    listing = ListingListSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'listing', 'buyer', 'seller', 'last_message', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last = obj.messages.order_by('-sent_at').first()
        return MessageSerializer(last).data if last else None
