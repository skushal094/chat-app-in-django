import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        """
        This method will add current socket connection to a particular group
        in the channels layer.
        Group name will be equal to the URL's kwargs as specified in the
        kwargs of the routing pattern. In this case, 'room_name' See routing pattern for this.

        Name of the group in the channels layer will be "chat_" + <room_name>
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        """
        Upon disconnection from the web socket, this method will remove the
        connected socket connection from the group that exists in the channels layer.
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        """
        This will be called each time when server receives a message from the socket client.
        This method will call the appropriate command (a function that will take action as per
        the action from the socket client).
        """
        data = json.loads(text_data)
        command = self.commands.get(data['command'])
        if command:
            command(self, data)

    def send_chat_message(self, message):
        """
        This method will send the `message` to the whole group that exists in the channel layer.
        So, if there are multiple users present in the group, then all of them will
        receive the message.

        To broadcast the message to everyone in the group.
        """
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def messages_to_json(self, messages):
        """
        This will call `message_to_json` and will return list of dictionary.
        :param messages: This will be a list/QuerySet of Message objects
        :return: list of dictionary where each dictionary will represent one message
        """
        result = []
        for message in messages:
            result.append(ChatConsumer.message_to_json(message))
        return result

    @staticmethod
    def message_to_json(message):
        """
        This will convert each Message object into dictionary which later will be sent
        to the socket client.
        :param message: Message object
        :return: dictionary with author, content, and timestamp keys.
        """
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.created_at)
        }

    def fetch_messages(self, data=None):
        """
        This will fetch last 10 messages from the DB and will call
        `messages_to_json` to convert them into list of dictionary.

        Calls `send_message` to send fetched messages to send to the client
        who wants last 10 messages (for ex., the one who just joined the chat room).
        """
        messages = Message.last_10_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data: dict):
        """
        This method will save the incoming message to the DB and will call
        `send_chat_message` to broadcast the message to everyone present in
        the group.
        :param data: dictionary having `from` and `message` keys
        :return:
        """
        author = data['from']
        # TODO handle if no user found with this `author` username
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(author=author_user, content=data['message'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def send_message(self, message):
        """
        First, this will convert the message into a JSON string.
        Then, this will send the `message` to the `fetch_messages` command
        requesting client only.
        """
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        """
        This will be called by the channel layer as this method is specified
        as a type in the `send_chat_message` method.
        """
        message = event['message']
        self.send(text_data=json.dumps(message))
