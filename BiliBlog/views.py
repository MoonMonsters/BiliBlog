#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-04-07 17:46
import datetime

from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache

from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, \
	get_7_days_hot_blogs, get_30_days_hot_blogs
from blog.models import Blog


def home(request):
	blog_content_type = ContentType.objects.get_for_model(Blog)
	# 得到每天中每天博客的阅读量以及对应的时间
	read_nums, dates = get_seven_days_read_data(blog_content_type)

	context = {}
	# 传到html中
	context['read_nums'] = read_nums
	context['dates'] = dates
	context['today_hot_data'], context['yesterday_hot_data'], context['seven_days_hot_data'], context[
		'thirty_days_hot_data'] = \
		get_datas_from_cache(blog_content_type)
	return render_to_response('home.html', context)


def get_datas_from_cache(blog_content_type):
	# 今天热门博客排行，一个小时更新一次
	today_hot_data = cache.get('today_hot_data')
	if not today_hot_data:
		today_hot_data = get_today_hot_data(blog_content_type)
		cache.set('today_hot_data', today_hot_data, 60 * 60)

	# 昨天热门博客缓存
	yesterday_hot_data = cache.get('yesterday_hot_data')
	if not yesterday_hot_data:
		yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
		cache.set('yesterday_hot_data', yesterday_hot_data, 60 * 60 * 24)

	# 7天热门博客缓存数据
	seven_days_hot_data = cache.get('seven_days_hot_data')
	# 如果缓存数据为空
	if not seven_days_hot_data:
		# 得到数据
		seven_days_hot_data = get_7_days_hot_blogs()
		# 并写入缓存，以及设置缓存时间，以秒为单位
		# 缓存到期后，便会自动删除缓存，然后便会为None了
		cache.set('seven_days_hot_data', seven_days_hot_data, 60 * 60 * 24)
	# 30天热门博客缓存
	thirty_days_hot_data = cache.get('thirty_days_hot_data')
	if not thirty_days_hot_data:
		thirty_days_hot_data = get_30_days_hot_blogs()
		cache.set('thirty_days_hot_data', thirty_days_hot_data, 60 * 60 * 24)

	return today_hot_data, yesterday_hot_data, seven_days_hot_data, thirty_days_hot_data
