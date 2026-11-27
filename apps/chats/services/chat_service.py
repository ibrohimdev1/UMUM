from django.core.exceptions import ValidationError, PermissionDenied
from apps.chats.repositories.chat_repository import ChatRepository
from apps.listings.repositories.listing_repository import ListingRepository

class ChatService:
    @classmethod
    def start_chat(cls, user, listing_id):
        listing = ListingRepository.get_by_id(listing_id)
        if not listing:
            raise ValidationError('E‘lon topilmadi.')

        if listing.user_id == user.id:
            raise ValidationError('O‘z e‘loningiz bilan chat ocha olmaysiz.')

        chat, _ = ChatRepository.get_or_create_chat(listing, buyer=user)
        return chat

    @classmethod
    def get_chat_for_user(cls, user, chat_id):
        chat = ChatRepository.get_by_id(chat_id, user)
        if not chat:
            raise PermissionDenied('Siz bu chat ishtirokchisi emassiz.')
        return chat

    @classmethod
    def send_message(cls, user, chat_id, body):
        chat = cls.get_chat_for_user(user, chat_id)
        if not body or not body.strip():
            raise ValidationError('Xabar bo‘sh bo‘lishi mumkin emas.')

        return ChatRepository.add_message(chat, sender=user, body=body.strip())
