from django.urls import path
from apps.chats.controllers.web.chats import ChatListView, ChatStartView

urlpatterns = [
    path('', ChatListView.as_view(), name='chats_list'),
    path('start/<int:listing_id>/', ChatStartView.as_view(), name='chat_start'),
]
