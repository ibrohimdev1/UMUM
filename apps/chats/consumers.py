import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f'chat_{self.chat_id}'
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_body = data.get('message', '').strip()

        if not message_body:
            return

        # Save to database
        msg = await self.save_message(self.chat_id, self.user.id, message_body)

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_id': msg['id'],
                'body': msg['body'],
                'sender_id': msg['sender_id'],
                'sender_name': msg['sender_name'],
                'sent_at': msg['sent_at'],
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, chat_id, user_id, body):
        from apps.chats.models import Chat, Message
        from apps.accounts.models import User
        user = User.objects.get(id=user_id)
        chat = Chat.objects.get(id=chat_id)
        msg = Message.objects.create(chat=chat, sender=user, body=body)
        return {
            'id': msg.id,
            'body': msg.body,
            'sender_id': user.id,
            'sender_name': user.full_name or user.phone,
            'sent_at': msg.sent_at.strftime('%H:%M'),
        }
