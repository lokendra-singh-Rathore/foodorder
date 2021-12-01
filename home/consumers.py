from channels.generic.websocket import WebsocketConsumer
import json
from  .models import *
from asgiref.sync import async_to_sync,sync_to_async

class OrderProgress(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['order_id']
        self.room_group_name = 'order_%s' % self.room_name
        print(self.room_group_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        order=Order.give_order_detail(self.room_name)
        print(order)
        self.send(text_data=json.dumps({
            'payload': order
        }))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
  
    def receive(self, text_data):
        

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'order_status',
                'payload': text_data
            }
        )

    # Receive message from room group
    def order_status(self, event):
        print(event)
        data = json.loads(event['value'])
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'payload': data
        }))