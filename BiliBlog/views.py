#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-04-07 17:46
from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType

from read_statistics.utils import get_seven_days_read_data
from blog.models import Blog


def home(request):
	blog_content_type = ContentType.objects.get_for_model(Blog)
	# 得到每天中每天博客的阅读量以及对应的时间
	read_nums, dates = get_seven_days_read_data(blog_content_type)

	context = {}
	# 传到html中
	context['read_nums'] = read_nums
	context['dates'] = dates
	return render_to_response('home.html', context)
