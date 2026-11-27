from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.exceptions import ValidationError
from apps.chats.models import Chat
from apps.chats.serializers import ChatSerializer, MessageSerializer
from apps.chats.services.chat_service import ChatService
from apps.chats.repositories.chat_repository import ChatRepository

class ChatListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chats = ChatRepository.get_user_chats(request.user)
        return Response(ChatSerializer(chats, many=True).data)

    def post(self, request):
        listing_id = request.data.get('listing_id')
        if not listing_id:
            return Response({'error': 'listing_id kiritilishi shart'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            chat = ChatService.start_chat(request.user, listing_id)
            return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e.message if hasattr(e, 'message') else e)}, status=status.HTTP_400_BAD_REQUEST)

class ChatMessageListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            chat = ChatService.get_chat_for_user(request.user, pk)
            messages = ChatRepository.get_messages(chat)
            return Response(MessageSerializer(messages, many=True).data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, pk):
        body = request.data.get('body')
        try:
            msg = ChatService.send_message(request.user, pk, body)
            return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
