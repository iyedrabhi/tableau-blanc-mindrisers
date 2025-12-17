import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        if user and user.is_authenticated:
            # join personal group
            self.user_group_name = f'user_{user.id}'
            await self.channel_layer.group_add(self.user_group_name, self.channel_name)

            # if staff, join managers group
            if user.is_staff:
                await self.channel_layer.group_add('managers', self.channel_name)

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        user = self.scope.get('user')
        if user and user.is_authenticated:
            await self.channel_layer.group_discard(self.user_group_name, self.channel_name)
            if user.is_staff:
                await self.channel_layer.group_discard('managers', self.channel_name)

    # Handler for notifications
    async def notification(self, event):
        # event should contain 'title' and 'message'
        await self.send(text_data=json.dumps({
            'title': event.get('title'),
            'message': event.get('message'),
            'type': event.get('notification_type')
        }))
