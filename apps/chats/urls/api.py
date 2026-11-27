from django.urls import path
from apps.chats.controllers.api.chats import ChatListCreateAPIView, ChatMessageListAPIView

urlpatterns = [
    path('', ChatListCreateAPIView.as_view(), name='api_chats_list_create'),
    path('<int:pk>/messages', ChatMessageListAPIView.as_view(), name='api_chat_messages'),
]
