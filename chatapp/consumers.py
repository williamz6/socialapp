
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self):
        await self.accept()

    async def receive(self, text_data):
        await self.send(text_data=text_data)
        print('received', text_data)

    async def disconnect(self, close_code):
        pass

""" 

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self, event):
        print('connected', event)
        await self.send({
            'type': 'websocket.accept',
        })

    async def receive(self, event):
       print('receive', event)

    async def disconnect(self, event):
        print('disconnect', event)

 """