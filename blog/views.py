from datetime import datetime

from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count

from .models import BlogType, Blog


def blogs_common_data(request, blogs):
	# 获取分页对象，将博客list传入，并设置每页数量
	paginator = Paginator(blogs, settings.EACH_PAGE_BLOGS_NUM)

	# 获取页码参数，从get请求获得，默认是第一页
	# .../?page=1
	page_num = request.GET.get('page', 1)
	# 从分页对象中，传入页码，获取每一页该有的数据
	page_of_blogs = paginator.get_page(page_num)
	# 获取当前页码，注意使用的对象时，从paginator对象中获取的分页对象
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

	blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
	blog_dates_dict = {}
	for blog_date in blog_dates:
		blog_count = Blog.objects.filter(created_time__year=blog_date.year,
		                                 created_time__month=blog_date.month).count()
		blog_dates_dict[blog_date] = blog_count

	context = {}
	# context['blogs'] = page_of_blogs.object_list
	context['page_range'] = page_range
	context['page_of_blogs'] = page_of_blogs
	context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
	context['blog_dates'] = blog_dates_dict

	return context


def blog_list(request):
	# 获取所有博客
	blogs_all = Blog.objects.all()
	context = blogs_common_data(request, blogs_all)
	# context['blogs_count'] = Blog.objects.all().count()
	return render_to_response('blog/blog_list.html', context)


def blog_detail(request, blog_pk):
	blog = get_object_or_404(Blog, pk=blog_pk)
	# 判断cookie中是否存储了文章阅读记录，如果没有，则+1
	if not request.COOKIES.get('blog_%s_read' % blog_pk, None):
		blog.read_num += 1
		blog.save()

	context = {}
	context['blog'] = blog
	# 上一篇博客，按时间顺序
	context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
	# 下一篇博客，可以直接使用first()方法来替代[0]
	context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
	response = render_to_response('blog/blog_detail.html', context)
	# 将文章是否已读写入cookie中，避免频繁刷新增加阅读记录
	# 等到浏览器关闭后，cookie才失效
	response.set_cookie('blog_%s_read' % blog_pk, 'true')
	return response


def blogs_with_type(request, blog_type_pk):
	blog_type = get_object_or_404(BlogType, pk=blog_type_pk)

	blogs_all = Blog.objects.filter(blog_type=blog_type)
	context = blogs_common_data(request, blogs_all)
	# context['blogs'] = page_of_blogs.object_list
	context['blog_type'] = blog_type
	return render_to_response('blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
	blogs_all = Blog.objects.filter(created_time__year=year, created_time__month=month)
	context = blogs_common_data(request, blogs_all)
	# context['blogs'] = page_of_blogs.object_list
	context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
	# context['blogs_count'] = Blog.objects.all().count()
	context['blogs_with_date'] = '%s年%s月' % (year, month)
	return render_to_response('blog/blogs_with_date.html', context)
