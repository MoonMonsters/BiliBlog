from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from ckeditor_uploader.fields import RichTextUploadingField
from DjangoUeditor.models import UEditorField

from read_statistics.models import ReadNumExpandMethod, ReadDetail


class BlogType(models.Model):
	type_name = models.CharField("博客类型", max_length=50)

	def __str__(self):
		return self.type_name

	class Meta:
		verbose_name = "博客类型"
		verbose_name_plural = verbose_name


class Blog(models.Model, ReadNumExpandMethod):
	title = models.CharField("标题", max_length=50)
	content = UEditorField(
		verbose_name="博客内容",
		width=1000,
		height=300,
		toolbars="full",
		imagePath="media/upload/image/%y/%m",
		filePath="media/upload/file/%y/%m",
		upload_settings={"imageMaxSize": 1204000},
		default="",
	)
	author = models.ForeignKey(User, verbose_name="作者", on_delete=models.DO_NOTHING)
	blog_type = models.ForeignKey(
		BlogType, verbose_name="博客类型", on_delete=models.DO_NOTHING
	)
	created_time = models.DateTimeField("创建时间", auto_now_add=True)
	last_update_time = models.DateTimeField("最后更新时间", auto_now=True)
	read_details = GenericRelation(ReadDetail)

	def __str__(self):
		return "<Blog:%s>" % self.title

	class Meta:
		ordering = ["-created_time"]
		verbose_name = "博客"
		verbose_name_plural = verbose_name
