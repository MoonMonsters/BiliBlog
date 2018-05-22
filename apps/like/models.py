from django.db import models
from django.contrib.auth.models import User

from blog.models import Blog


class BlogLike(models.Model):
	# 点赞用户
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# 点赞博客
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
