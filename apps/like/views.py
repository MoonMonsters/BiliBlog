from django.shortcuts import render
from django.contrib import auth
from django.http import JsonResponse

from .models import BlogLike
from blog.models import Blog


def give_blog_a_like(request):
	"""
	不用login_required进行验证
	:param blog_id: 博客id
	:return: 验证后的数据
	"""
	data = dict()
	if request.user.is_authenticated:
		blog_id = request.GET.get('blog_id', -1)
		data['status'] = 'SUCCESS'
		blog_like = BlogLike.objects.filter(blog_id=blog_id, user=request.user)
		# 如果该用户已对该博客点过赞，则取消赞
		if blog_like.exists():
			data['type'] = 'unlike'
			# 取消点赞，删除数据
			blog_like.delete()
		else:
			data['type'] = 'like'
			# 保存数据
			BlogLike.objects.create(blog=Blog.objects.filter(pk=blog_id).first(), user=request.user)
	else:
		data['status'] = 'ERROR'
		data['description'] = '未登录，不可点赞'

	return JsonResponse(data)
