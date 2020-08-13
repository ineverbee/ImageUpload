from django.db import models
import os

# Create your models here.
class ImageModel(models.Model):

	class Meta:
		verbose_name = 'Image'
		verbose_name_plural = 'Images'

	img = models.ImageField(upload_to='static/', blank=True)
	url = models.TextField(blank=True, max_length=200)
	width = models.IntegerField(blank=True, null=True)
	height = models.IntegerField(blank=True, null=True)

	def __str__(self):
		if self.url != '':
			return self.url
		else:
			return self.img.url
