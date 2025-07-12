import json
from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

@database_sync_to_async
def _get_message_unread_count(user_id):
    """获取用户的未读消息数量"""
    from mysystem.models import NotificationUsers
    count = NotificationUsers.objects.filter(user_id=user_id, is_read=False).count()
    return count or 0

def set_message(sender, msg_type, msg, unread=0):
    text = {
        'sender': sender,
        'msg_type': msg_type,
        'content': msg,
        'unread': unread
    }
    return text


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            self.user = self.scope.get('user',None)
            room_name = "user_" + str(self.user.id)
            self.room_group_name = f'notifications_{room_name}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept("JWTLYADMIN")
            
            unread_count = await _get_message_unread_count(self.user)
            if unread_count == 0:
                await self.send_json(set_message('system', 'SYS', f'{self.user.name}，你好！消息通知已上线！'))
            else:
                await self.send_json(set_message('system', 'SYS', "请查看您的未读消息~",unread=unread_count))
        except Exception as e:
            await self.close()
    
    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        pass

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        try:
            await self.close(close_code)
        except Exception:
            pass

    async def push_message(self, event):
        message = event['json']
        await self.send(text_data=json.dumps(message))