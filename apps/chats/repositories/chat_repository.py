from django.db.models import Q
from apps.chats.models import Chat, Message

class ChatRepository:
    @staticmethod
    def get_or_create_chat(listing, buyer):
        chat, created = Chat.objects.get_or_create(
            listing=listing,
            buyer=buyer,
            defaults={'seller': listing.user}
        )
        return chat, created

    @staticmethod
    def get_user_chats(user):
        return Chat.objects.filter(Q(buyer=user) | Q(seller=user)).select_related('listing', 'buyer', 'seller').prefetch_related('messages').order_by('-updated_at')

    @staticmethod
    def get_by_id(chat_id, user):
        return Chat.objects.filter(
            id=chat_id
        ).filter(Q(buyer=user) | Q(seller=user)).select_related('listing', 'buyer', 'seller').first()

    @staticmethod
    def get_messages(chat):
        return Message.objects.filter(chat=chat).select_related('sender').order_by('sent_at')

    @staticmethod
    def add_message(chat, sender, body):
        return Message.objects.create(chat=chat, sender=sender, body=body)
