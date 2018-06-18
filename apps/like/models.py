from django.db import models
from django.contrib.auth.models import User

from blog.models import Blog


class BlogLike(models.Model):
	# 点赞用户
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# 点赞博客
	blog = models.ForeignKey(Blog, verbose_name='博客', on_delete=models.CASCADE)

	def __str__(self):
		return '{0} like {1}'.format(self.user, self.blog)

	class Meta:
		verbose_name = '点赞'
		verbose_name_plural = verbose_name
