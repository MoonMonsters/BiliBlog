from django.db import models
from django.contrib.auth.models import User

class IPSaver(models.Model):
	ip = models.CharField(max_length=16, default='127.0.0.1')
	blog_id = models.IntegerField(default=-1)
	visited_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = '访问IP'
		verbose_name_plural = verbose_name
