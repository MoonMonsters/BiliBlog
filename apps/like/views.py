import threading

from django.http import JsonResponse
from django import views

from .models import BlogLike
from blog.models import Blog

# 使用Condition()替代Lock()
condition = threading.Condition()


class GiveBlogALike(views.View):
	def get(self, request):
		return self.give_blog_a_like(request)

	def give_blog_a_like(self, request):
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
			# 将此部分代码锁住，避免在同一个人在多时间重复多次点击时，出现加了很多次或者出现负数的情况
			# 虽然点击完成后，数据还是正常的
			with condition:
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
			data['description'] = '请先登录再点赞'

		return JsonResponse(data)
