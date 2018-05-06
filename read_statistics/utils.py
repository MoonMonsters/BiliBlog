#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-05-05 21:11
import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum

from .models import ReadNum, ReadDetail
from blog.models import Blog


def read_statistics_once_read(request, obj):
	# obj是传入的实例对象
	ct = ContentType.objects.get_for_model(obj)
	# 构建cookie的key值
	key = '%s_%s_read' % (ct.model, obj.pk)

	# 如果该key值cookie中不存在
	if not request.COOKIES.get(key):
		# get_or_create函数，会返回一个tuple
		readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
		# 这个值默认是0，则+1
		readnum.read_num += 1
		# 保存
		readnum.save()

		# 当天阅读量+1
		date = timezone.now().date()
		read_detail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
		read_detail.read_num += 1
		read_detail.save()

	# 返回应该存入cookie的key值
	return key


def get_seven_days_read_data(content_type):
	# 得到当前时间
	today = timezone.now().date()
	# 每天的博客阅读总量
	read_nums = []
	# 对应时间
	dates = []
	for i in range(6, -1, -1):
		# 利用偏差计算前几天的时间
		date = today - datetime.timedelta(days=i)
		# 格式化
		dates.append(date.strftime('%m/%d'))
		read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
		# 利用聚合计算阅读总量
		result = read_details.aggregate(read_num_sum=Sum('read_num'))
		# 如果阅读量为空，则设置成0
		read_nums.append(result['read_num_sum'] or 0)

	return read_nums, dates


def get_today_hot_data(content_type):
	today = timezone.now().date()
	# 排序，按照从大到小的顺序
	read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')

	return read_details[:7]


def get_yesterday_hot_data(content_type):
	today = timezone.now().date()
	yesterday = today - datetime.timedelta(days=1)
	read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')

	return read_details[:7]


def get_7_days_hot_blogs():
	today = timezone.now().date()
	date = today - datetime.timedelta(days=7)
	blogs = Blog.objects \
		.filter(read_details__date__lte=today, read_details__date__gte=date) \
		.values('id', 'title') \
		.annotate(read_num_sum=Sum('read_details__read_num')) \
		.order_by('-read_details__read_num')
	return blogs[:7]


def get_30_days_hot_blogs():
	today = timezone.now().date()
	date = today - datetime.timedelta(days=30)
	blogs = Blog.objects \
		.filter(read_details__date__lte=today, read_details__date__gte=date) \
		.values('id', 'title') \
		.annotate(read_num_sum=Sum('read_details__read_num')) \
		.order_by('-read_details__read_num')
	return blogs[:7]
