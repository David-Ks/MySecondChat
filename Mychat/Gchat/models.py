from django.db import models

class roomModel(models.Model):
	room_name = models.CharField(max_length=150, verbose_name='Room name')

	def __str__(self):
		return self.room_name 
