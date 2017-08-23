from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import User
import os


# Create your models here.
class Files(models.Model):
	title = models.CharField(max_length = 100, help_text="Title of the document/video.")
	file = models.FileField(upload_to='uploads/%Y/%m/%d/')
	slug = models.SlugField(max_length = 100, unique = True, help_text = "Automatically generated text for links, please make sure it's unique for files with same name.")
	def __unicode__(self):
		return self.title
	def extenstion(self):
		name, extension = os.path.splitext(self.file.name)
		return extension

class FileViewing(models.Model):
	user = models.ForeignKey(User)
	file = models.ForeignKey(Files)
	timestamp = models.DateTimeField(auto_now_add=True)
	seconds_viewed = models.IntegerField(default=0)


class ViewingPermissionToken(models.Model):
	user = models.ForeignKey(User)
	file = models.ForeignKey(Files)
	timestamp = models.DateTimeField(auto_now_add=True)
	id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)