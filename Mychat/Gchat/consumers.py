import json
from .models import *
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'chat_%s' % self.room_name

		getRoom = await self.get_rooms(self.room_name)
		if getRoom:       
			await self.channel_layer.group_add(
					self.room_group_name,
					self.channel_name
				)

			await self.accept()

	@database_sync_to_async
	def get_rooms(self, e):
		try:
			z = roomModel.objects.get(room_name=e)
			return True
		except:
			return False

	async def disconnect(self, close_code):

		await self.channel_layer.group_discard(
				self.room_group_name,
				self.channel_name
			)

	@database_sync_to_async
	def get_user_name(self):
		user = self.scope['user']
		if user.is_anonymous:
			return 'Anonymous'
		else:
			return user

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		userSname = await self.get_user_name()

		await self.channel_layer.group_send(
				self.room_group_name,
				{
					'type': 'chat_message',
					'message': f"<{str(userSname)}>: " + message
				}
			)

	async def chat_message(self, event):
		message = event['message']
		userSname = await self.get_user_name()

		await self.send(
				text_data = json.dumps({'message': message})
			)