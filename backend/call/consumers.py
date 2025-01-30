import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import CallSession

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"] == AnonymousUser():
            await self.close()
            return
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        # join the group
        await self.channel_layer.group_add(self.session_id, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.session_id, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # broadcast to group
        await self.channel_layer.group_send(
            self.session_id,
            {
                'type': 'signal_message',
                'data': data,
                'sender_channel': self.channel_name
            }
        )

    async def signal_message(self, event):
        # don't echo back to self
        if event['sender_channel'] != self.channel_name:
            await self.send(text_data=json.dumps(event['data']))
