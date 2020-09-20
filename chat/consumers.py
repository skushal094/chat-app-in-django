import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect 123")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print("disconnect 123")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        await self.commands[data['command']](self, data)

    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(ChatConsumer.message_to_json(message))
        return result

    @staticmethod
    def message_to_json(message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.created_at)
        }

    async def fetch_messages(self, data):
        messages = await self.get_last_10_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        await self.send_message(content)

    async def new_message(self, data):
        author = data['from']
        author_user = await self.get_user_for_message(username=author)
        message = await self.create_message(author=author_user, content=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return await self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def create_message(self, author=None, content=None):
        return Message.objects.create(author=author, content=content)

    @database_sync_to_async
    def get_user_for_message(self, username=None):
        return User.objects.filter(username=username)[0]

    @database_sync_to_async
    def get_last_10_messages(self):
        return Message.last_10_messages()
