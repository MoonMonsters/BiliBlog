#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-02 12:21
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.conf import settings

from blog.models import Blog
from read_statistics.utils import get_today_hot_data, get_yesterday_hot_data, \
	get_7_days_hot_blogs, get_30_days_hot_blogs


def get_datas_from_cache(blog_content_type, type):
	context = dict()
	hot_datas = None
	hot_type = None
	type = int(type)
	if type == 0:
		# 今天热门博客排行，一个小时更新一次
		# today_hot_data = cache.get('today_hot_data')
		today_hot_data = None
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
