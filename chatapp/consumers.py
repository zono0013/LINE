import hashlib
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{hashlib.md5(self.room_name.encode("utf-8")).hexdigest()}'
        print("Room name(consumers):", self.room_name)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        currentRoomName = text_data_json['room']
        user = text_data_json['user']
        if currentRoomName is not None:
            print("Room name2:", currentRoomName)
        else:
            print("Room name is not provided in the message.")

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': user,
                'room': currentRoomName,
                'message': message
            }
        )

    def chat_message(self, event):
        user = event['user']
        message = event['message']
        room = event['room']
        print(message, room)
        self.send(text_data=json.dumps({
            'type': 'chat',
            'user': user,
            'room': room,
            'message': message
        }))
        