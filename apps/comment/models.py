from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Comment(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	text = models.TextField()
	comment_time = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

	class Meta:
		ordering = ['-comment_time']


class NewCommentCount(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	count = models.IntegerField(default=0)

	def __str__(self):
		return self.user.username + ', count = ' + str(self.count)

	def increase_count(self):
		"""
		评论数+1
		"""
		print('self.count = ', self.count)
		self.count += 1
		self.save()

	def clear_count(self):
		"""
		清空评论数
		"""
		self.count = 0
		self.save()
