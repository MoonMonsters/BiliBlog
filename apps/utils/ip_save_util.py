#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-06-23 0:10


from api.models import IPSaver


def save_ip(request, blog_id):
	"""
	保存访问者的IP
	:param request: 请求对象
	:param blog_id: 博客id，如果是主页，那么就是-1
	:return:
	"""
	# print(request.META)
	if 'HTTP_X_FORWARDED_FOR' in request.META:
		ip = request.META['HTTP_X_FORWARDED_FOR']
	else:
		ip = request.META['REMOTE_ADDR']
	print('ip = ', ip)
	IPSaver.objects.create(ip=ip, blog_id=blog_id)
