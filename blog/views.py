from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings

from .models import BlogType, Blog


def blog_list(request):
	blogs_all = Blog.objects.all()
	# 每10页进行分页
	paginator = Paginator(blogs_all, settings.EACH_PAGE_BLOGS_NUM)

	# 获取页码参数，get请求，默认是第一页
	page_num = request.GET.get('page', 1)
	page_of_blogs = paginator.get_page(page_num)

	current_page_num = page_of_blogs.number
	# page_range = [current_page_num - 2, current_page_num - 1, current_page_num + 1, current_page_num + 2]
	# 获取当前页码的前后两页
	page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
	             list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

	# 加上省略页码标记
	if page_range[0] - 1 >= 2:
		page_range.insert(0, '...')
	if paginator.num_pages - page_range[-1] >= 2:
		page_range.append('...')

	# 加上首页和尾页
	if page_range[0] != 1:
		page_range.insert(0, 1)
	if page_range[-1] != paginator.num_pages:
		page_range.append(paginator.num_pages)

	context = {}
	# context['blogs'] = page_of_blogs.object_list
	context['page_range'] = page_range
	context['page_of_blogs'] = page_of_blogs
	context['blog_types'] = BlogType.objects.all()
	# context['blogs_count'] = Blog.objects.all().count()
	return render_to_response('blog/blog_list.html', context)


def blog_detail(request, blog_pk):
	context = {}
	context['blog'] = get_object_or_404(Blog, pk=blog_pk)

	return render_to_response('blog/blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
	blog_type = get_object_or_404(BlogType, pk=blog_type_pk)

	blogs_all = Blog.objects.filter(blog_type=blog_type)
	# 每10页进行分页
	paginator = Paginator(blogs_all, settings.EACH_PAGE_BLOGS_NUM)

	# 获取页码参数，get请求，默认是第一页
	page_num = request.GET.get('page', 1)
	page_of_blogs = paginator.get_page(page_num)

	current_page_num = page_of_blogs.number
	# page_range = [current_page_num - 2, current_page_num - 1, current_page_num + 1, current_page_num + 2]
	# 获取当前页码的前后两页
	page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
	             list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

	# 加上省略页码标记
	if page_range[0] - 1 >= 2:
		page_range.insert(0, '...')
	if paginator.num_pages - page_range[-1] >= 2:
		page_range.append('...')

	# 加上首页和尾页
	if page_range[0] != 1:
		page_range.insert(0, 1)
	if page_range[-1] != paginator.num_pages:
		page_range.append(paginator.num_pages)

	context = {}
	# context['blogs'] = page_of_blogs.object_list
	context['page_range'] = page_range
	context['page_of_blogs'] = page_of_blogs
	context['blog_type'] = blog_type
	context['blog_types'] = BlogType.objects.all()
	# context['blogs_count'] = Blog.objects.all().count()
	return render_to_response('blog/blogs_with_type.html', context)
