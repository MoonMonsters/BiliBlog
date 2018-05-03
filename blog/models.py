from django.db import models
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class BlogType(models.Model):
	type_name = models.CharField(max_length=50)

	def __str__(self):
		return self.type_name


class Blog(models.Model):
	title = models.CharField(max_length=50)
	content = RichTextUploadingField()
	author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
	created_time = models.DateTimeField(auto_now_add=True)
	last_update_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '<Blog:%s>' % self.title

	class Meta:
		ordering = ['-created_time']
