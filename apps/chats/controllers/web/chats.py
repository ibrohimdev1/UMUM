from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.chats.services.chat_service import ChatService
from apps.chats.repositories.chat_repository import ChatRepository

class ChatListView(LoginRequiredMixin, View):
    template_name = 'chats/list.html'

    def get(self, request):
        chats = ChatRepository.get_user_chats(request.user)
        active_chat = None
        messages = []

        chat_id = request.GET.get('chat_id')
        if chat_id:
            active_chat = ChatService.get_chat_for_user(request.user, chat_id)
            messages = ChatRepository.get_messages(active_chat)
        elif chats.exists():
            active_chat = chats.first()
            messages = ChatRepository.get_messages(active_chat)

        return render(request, self.template_name, {
            'chats': chats,
            'active_chat': active_chat,
            'messages': messages,
        })

class ChatStartView(LoginRequiredMixin, View):
    def get(self, request, listing_id):
        chat = ChatService.start_chat(request.user, listing_id)
        return redirect(f"/chats/?chat_id={chat.id}")
