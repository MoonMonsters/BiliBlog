from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from .models import Comment


def update_comment(request):
	"""
	处理评论内容
	"""
	# 从META中，可以根据HTTP_REFERER获取是从哪个网页中提交的内容，获得网页地址
	referer = request.META.get('HTTP_REFERER', reverse('home'))

	user = request.user
	# 判断提交评论时，用户是否已经登录
	if not user.is_authenticated:
		return render(request, 'error.html', {'message': '用户未登录', 'redirect_to': referer})
	text = request.POST.get('text', '').strip()
	if text == '':
		return render(request, 'error.html', {'message': '评论内容为空', 'redirect_to': referer})

	try:
		# 从提交中获得content_type和object_id
		content_type = request.POST.get('content_type', '')
		object_id = int(request.POST.get('object_id', ''))
		# 根据content_type获取Blog类的实例，而不是对象实例
		model_class = ContentType.objects.get(model=content_type).model_class()
		# 获取blog对象
		model_obj = model_class.objects.get(pk=object_id)
	except Exception:
		return render(request, 'error.html', {'message': '评论对象不存在', 'redirect_to': referer})
	# 保存评论
	comment = Comment()
	# 评论者
	comment.user = user
	# 评论内容
	comment.text = text
	# 评论的博客
	comment.content_object = model_obj
	comment.save()
	# 评论完后，回到之前的页面
	return redirect(referer)
