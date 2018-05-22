from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.conf import settings

from .models import BlogType, Blog
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm
from read_statistics.utils import get_today_hot_data, get_yesterday_hot_data, \
	get_7_days_hot_blogs, get_30_days_hot_blogs
from like.models import BlogLike


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
	print('blog_dates = ', blog_dates)
	blog_dates_dict = {}
	for blog_date in blog_dates:
		# 按照年份和月份过滤Blog数据并且分组计算数量
		blog_count = Blog.objects.filter(created_time__year=blog_date.year,
		                                 created_time__month=blog_date.month).count()
		blog_dates_dict[blog_date] = blog_count

	context = dict()
	# 页数列表
	context['page_range'] = page_range
	# 每页数据
	context['page_of_blogs'] = page_of_blogs
	# 聚合
	# 得到BlogType的QuerySet对象，<QuerySet [<BlogType: 感悟>, <BlogType: 随笔>, <BlogType: Django>]>
	# 使用对象，例如 q[0].blog_count可以得到 感悟 类型中，blog的数量
	context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
	# 得到按照时间分类的每个时间点的数据
	context['blog_dates'] = blog_dates_dict

	return context


def blog_list(request):
	# 获取所有博客
	blogs_all = Blog.objects.all()
	context = blogs_common_data(request, blogs_all)
	# context['blogs_count'] = Blog.objects.all().count()

	return render(request, 'blog/blog_list.html', context)


def blog_detail(request, blog_pk):
	blog = get_object_or_404(Blog, pk=blog_pk)
	# 在博客文章详情页中，取得应该存入cookie中的key值
	read_cookie_key = read_statistics_once_read(request, blog)
	blog_content_type = ContentType.objects.get_for_model(blog)
	# 获取该博客下所有评论
	comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)

	context = dict()
	context['blog'] = blog
	# 上一篇博客，按时间顺序
	context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
	# 下一篇博客，可以直接使用first()方法来替代[0]
	context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
	# 传到html中
	context['comments'] = comments
	data = dict()
	data['content_type'] = blog_content_type.model
	data['object_id'] = blog_pk
	data['user'] = request.user
	# 创建时CommentForm对象时，同事传入初始数据
	context['comment_form'] = CommentForm(initial=data)
	if request.user.is_authenticated:
		# 从request中读取到user数据，并结合博客id，判断登录用户是否对这篇博客点赞了
		context['blog_like_active'] = BlogLike.objects.filter(blog_id=blog_pk, user=request.user).exists()
	context['blog_like_count'] = BlogLike.objects.filter(blog_id=blog_pk).count()
	# context['user'] = request.user
	response = render(request, 'blog/blog_detail.html', context)
	# 将文章是否已读写入cookie中，避免频繁刷新增加阅读记录
	# 等到浏览器关闭后，cookie才失效
	response.set_cookie(read_cookie_key, 'true')
	return response


def blogs_with_type(request, blog_type_pk):
	blog_type = get_object_or_404(BlogType, pk=blog_type_pk)

	blogs_all = Blog.objects.filter(blog_type=blog_type)
	context = blogs_common_data(request, blogs_all)
	# context['blogs'] = page_of_blogs.object_list
	context['blog_type'] = blog_type

	for index, bt in enumerate(context['blog_types']):
		if bt == blog_type:
			# 得到每种类型博客数量
			context['blog_every_type_count'] = context['blog_types'][index].blog_count
			break
	else:
		# 如果出意外，则设置为0
		context['blog_every_type_count'] = 0

	return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
	# 根据年月得到所有博客
	blogs_all = Blog.objects.filter(created_time__year=year, created_time__month=month)
	context = blogs_common_data(request, blogs_all)
	# context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
	context['blogs_with_date'] = '%s年%s月' % (year, month)
	return render(request, 'blog/blogs_with_date.html', context)


def blogs_hot(request, type):
	"""
	获取热门博客列表
	:param type: 0：今日 1：昨日 2：七天 3：三十天
	"""
	blog_content_type = ContentType.objects.get_for_model(Blog)
	context = get_datas_from_cache(blog_content_type, type)
	print('-' * 80)
	for data in context['hot_datas']:
		print(data)
	print('-' * 80)

	return render(request, 'blog/blog_hot.html', context=context)


def get_datas_from_cache(blog_content_type, type):
	context = dict()
	hot_datas = None
	hot_type = None
	if type == 0:
		# 今天热门博客排行，一个小时更新一次
		today_hot_data = cache.get('today_hot_data')
		if not today_hot_data:
			today_hot_data = get_today_hot_data(blog_content_type)
			cache.set('today_hot_data', today_hot_data, settings.CACHE_TIME_TODAY)

		hot_datas = [Blog.objects.get(pk=read_detail.object_id) for read_detail in today_hot_data]
		hot_type = '今日热门博客'
	elif type == 1:
		# 昨天热门博客缓存
		yesterday_hot_data = cache.get('yesterday_hot_data')
		if not yesterday_hot_data:
			yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
			cache.set('yesterday_hot_data', yesterday_hot_data, settings.CACHE_TIME_YESTERDAY)
		hot_type = '昨日热门博客'
		hot_datas = [Blog.objects.get(pk=read_detail.object_id) for read_detail in yesterday_hot_data]
	elif type == 2:
		# 7天热门博客缓存数据
		seven_days_hot_data = cache.get('seven_days_hot_data')
		# 如果缓存数据为空
		if not seven_days_hot_data:
			# 得到数据
			seven_days_hot_data = get_7_days_hot_blogs()
			# 并写入缓存，以及设置缓存时间，以秒为单位
			# 缓存到期后，便会自动删除缓存，然后便会为None了
			cache.set('seven_days_hot_data', seven_days_hot_data, settings.CACHE_TIME_SEVEN_DAY)
		hot_type = '七日热门博客'
		hot_datas = [Blog.objects.get(pk=data['id']) for data in seven_days_hot_data]
	elif type == 3:
		# 30天热门博客缓存
		thirty_days_hot_data = cache.get('thirty_days_hot_data')
		if not thirty_days_hot_data:
			thirty_days_hot_data = get_30_days_hot_blogs()
			cache.set('thirty_days_hot_data', thirty_days_hot_data, settings.CACHE_TIME_THIRTY_DAY)
		hot_type = '三十日热门博客'
		hot_datas = [Blog.objects.get(pk=data['id']) for data in thirty_days_hot_data]

	context['hot_datas'] = hot_datas
	context['hot_type'] = hot_type
	return context
