from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from DjangoUeditor.models import UEditorField


class Comment(models.Model):
	content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
	object_id = models.PositiveIntegerField('博客ID')
	content_object = GenericForeignKey('content_type', 'object_id')

	text = UEditorField(
		verbose_name="评论内容",
		width=1000,
		height=300,
		toolbars="full",
		imagePath="media/upload/image/%y/%m",
		filePath="media/upload/file/%y/%m",
		upload_settings={"imageMaxSize": 1204000},
		default="",
	)
	comment_time = models.DateTimeField('评论时间', auto_now_add=True)
	user = models.ForeignKey(User, verbose_name='被评论者', on_delete=models.DO_NOTHING)

	class Meta:
		ordering = ['-comment_time']
		verbose_name = '评论'
		verbose_name_plural = verbose_name


class NewCommentCount(models.Model):
	user = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING, editable=False)
	count = models.IntegerField('新评论数', default=0, editable=False)

	def __str__(self):
		return self.user.username + ', count = ' + str(self.count)

	class Meta:
		verbose_name = '新评论数'
		verbose_name_plural = verbose_name

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
